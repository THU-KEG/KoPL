import json
import os
from collections import defaultdict
from queue import Queue
from datetime import date
from tqdm import tqdm
from kopl.util import ValueClass, comp



class KB(object):
	def __init__(self, kb):
		self.entities = {}
		for cid in kb['concepts']:
			self.entities[cid] = kb['concepts'][cid]
			self.entities[cid]['relations'] = []
			self.entities[cid]['attributes'] = []
			self.entities[cid]['isA'] = self.entities[cid].pop('subclassOf')
		for eid in kb['entities']:
			self.entities[eid] = kb['entities'][eid]
			self.entities[eid]['isA'] = self.entities[eid].pop('instanceOf')
		print('process concept')
		self.name_to_id = defaultdict(list) # id 包含 concept 和 entity
		self.concept_to_entity = defaultdict(set)
		for ent_id, ent_info in tqdm(self.entities.items()):
			self.name_to_id[ent_info['name']].append(ent_id)
			for c in self.get_all_concepts(ent_id): # merge entity into ancestor concept
				self.concept_to_entity[c].add(ent_id)
		self.concept_to_entity = { k:list(v) for k,v in self.concept_to_entity.items() }
		self.concepts = list(self.concept_to_entity.keys())

		print('process attribute and relation')
		# get all attribute keys and relations
		self.attribute_keys = set()
		self.relations = set()
		self.key_type = {}
		'''
		{
			<attribute key>: {
				<entity id>: [idx1, idx2], # index in self.entities[ent_id]['attributes']
			}
		}
		'''
		
		self.attribute_inv_index = defaultdict(lambda: defaultdict(list))
		# self.attribute_inv_index = {}
		'''
		{
			(relation, direction): {
				<entity id>: [idx1, idx2], # index in self.entities[ent_id]['relations']
			}
		}
		'''
		self.relation_inv_index = defaultdict(lambda: defaultdict(list))
		# self.relation_inv_index = {}
		'''
		{
			(sub_id, obj_id): [idx1, idx2] # index in self.entities[sub_id]['relations']
		}
		'''
		self.forward_relation_index = defaultdict(list)

		# store entities that have attribute
		self.entity_set_with_attribute = set()
		# store entities that have quantity attribute
		self.entity_set_with_quantity_attribute = set()
		# store entities that have attribute qualifier
		self.entity_set_with_attribute_qualifier = set()
		# store entities that have relation
		self.entity_set_with_relation = set()
		# store entities that have relation qualifier
		self.entity_set_with_relation_qualifier = set()
		for ent_id, ent_info in tqdm(self.entities.items()):
			for idx, attr_info in enumerate(ent_info['attributes']):
				self.attribute_keys.add(attr_info['key'])
				self.key_type[attr_info['key']] = attr_info['value']['type']
				self.attribute_inv_index[attr_info['key']][ent_id].append(idx)
				self.entity_set_with_attribute.add(ent_id)
				if attr_info['value']['type'] == 'quantity':
					self.entity_set_with_quantity_attribute.add(ent_id)
				for qk in attr_info['qualifiers']:
					self.attribute_keys.add(qk)
					self.entity_set_with_attribute_qualifier.add(ent_id)
					for qv in attr_info['qualifiers'][qk]:
						self.key_type[qk] = qv['type']

			for idx, rel_info in enumerate(ent_info['relations']):
				self.relations.add(rel_info['relation'])
				self.relation_inv_index[(rel_info['relation'], rel_info['direction'])][ent_id].append(idx)
				if rel_info['direction'] == 'forward':
					self.forward_relation_index[(ent_id, rel_info['object'])].append(idx)
				self.entity_set_with_relation.add(ent_id)
				for qk in rel_info['qualifiers']:
					self.attribute_keys.add(qk)
					self.entity_set_with_relation_qualifier.add(ent_id)
					for qv in rel_info['qualifiers'][qk]:
						self.key_type[qk] = qv['type']

			# parse values into ValueClass object
			for attr_info in ent_info['attributes']:
				attr_info['value'] = self._parse_value(attr_info['value'])
				for qk, qvs in attr_info['qualifiers'].items():
					attr_info['qualifiers'][qk] = [self._parse_value(qv) for qv in qvs]
			for rel_info in ent_info['relations']:
				for qk, qvs in rel_info['qualifiers'].items():
					rel_info['qualifiers'][qk] = [self._parse_value(qv) for qv in qvs]

		self.attribute_keys = list(self.attribute_keys)
		self.relations = list(self.relations)
		# Note: key_type is one of string/quantity/date, but date means the key may have values of type year
		self.key_type = { k:v if v!='year' else 'date' for k,v in self.key_type.items() }
		self.entity_set_with_both_attribute_and_relation = list(self.entity_set_with_attribute & self.entity_set_with_relation)
		self.entity_set_with_attribute = list(self.entity_set_with_attribute)
		self.entity_set_with_quantity_attribute = list(self.entity_set_with_quantity_attribute)
		self.entity_set_with_attribute_qualifier = list(self.entity_set_with_attribute_qualifier)
		self.entity_set_with_relation = list(self.entity_set_with_relation)
		self.entity_set_with_relation_qualifier = list(self.entity_set_with_relation_qualifier)

		print('extract seen values')
		self.key_values = defaultdict(set)
		self.concept_key_values = defaultdict(lambda: defaultdict(set)) # not include qualifier values
		self.concept_relations = defaultdict(lambda: defaultdict(list))

		for ent_id, ent_info in tqdm(self.entities.items()):
			for attr_info in ent_info['attributes']:
				k, v = attr_info['key'], attr_info['value']
				self.key_values[k].add(v)
				for c in self.get_all_concepts(ent_id):
					self.concept_key_values[c][k].add(v)
				# merge qualifier statistics into attribute
				for qk, qvs in attr_info['qualifiers'].items():
					for qv in qvs:
						self.key_values[qk].add(qv)

			for rel_info in ent_info['relations']:
				for c in self.get_all_concepts(ent_id):
					self.concept_relations[c][(rel_info['relation'], rel_info['direction'])].append(rel_info['object'])
				# merge qualifier statistics into attribute
				for qk, qvs in rel_info['qualifiers'].items():
					for qv in qvs:
						self.key_values[qk].add(qv)
		for k in self.key_values:
			self.key_values[k] = list(self.key_values[k])
		for c in self.concept_key_values:
			for k in self.concept_key_values[c]:
				self.concept_key_values[c][k] = list(self.concept_key_values[c][k])
	
		print('number of concepts: %d' % len(self.concepts))
		print('number of entities: %d' % len(self.entities))
		print('number of attribute keys: %d' % len(self.attribute_keys))
		print('number of relations: %d' % len(self.relations))

	def get_direct_concepts(self, ent_id):
		"""
		return the direct concept id of given entity/concept
		"""
		if ent_id in self.entities:
			return [i for i in self.entities[ent_id]['isA'] if i in self.entities and i != ent_id]
		else:
			return []
			# raise Exception('unknown id')

	def get_all_concepts(self, ent_id):
		"""
		return a concept id list
		"""
		ancestors = set()
		q = Queue()
		for c in self.get_direct_concepts(ent_id):
			q.put(c)
		while not q.empty():
			con_id = q.get()
			if con_id in self.entities and con_id not in ancestors: # 防止循环祖先的情况
				ancestors.add(con_id)
				for c in self.entities[con_id]['isA']:
					q.put(c)
		ancestors = list(ancestors)
		return ancestors

	def print_statistics(self):
		cnt_rel, cnt_attr, cnt_qual = 0, 0, 0
		for ent_id, ent_info in self.entities.items():
			for attr_info in ent_info['attributes']:
				cnt_attr += 1
				for qk in attr_info['qualifiers']:
					for qv in attr_info['qualifiers'][qk]:
						cnt_qual += 1
		for ent_id, ent_info in self.entities.items():
			for rel_info in ent_info['relations']:
				cnt_rel += 1
				for qk in rel_info['qualifiers']:
					for qv in rel_info['qualifiers'][qk]:
						cnt_qual += 1

		print('number of relation knowledge: %d' % cnt_rel)
		print('number of attribute knowledge: %d' % cnt_attr)
		print('number of qualifier knowledge: %d' % cnt_qual)

	def _parse_value(self, value):
		if value['type'] == 'string':
			result = ValueClass('string', value['value'])
		elif value['type'] == 'quantity':
			result = ValueClass('quantity', (float)(value['value']), value['unit'])
		else:
			x = str(value['value'])
			if '/' in x or ('-' in x and '-' != x[0]):
				split_char = '/' if '/' in x else '-'
				p1, p2 = x.find(split_char), x.rfind(split_char)
				y, m, d = int(x[:p1]), int(x[p1+1:p2]), int(x[p2+1:])
				result = ValueClass('date', date(y, m, d))
			else:
				result = ValueClass('year', (int)(x))
		return result