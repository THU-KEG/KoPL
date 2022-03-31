import json
import os
from collections import defaultdict, Counter
from queue import Queue
from datetime import date
from tqdm import tqdm
from kopl.data import KB
from kopl.util import ValueClass, comp




class KoPLEngine(object):
	def __init__(self, kb):
		self.kb = KB(kb)
		
	def _parse_key_value(self, key, value, typ=None):
		if typ is None:
			typ = self.kb.key_type[key]
		if typ=='string':
			value = ValueClass('string', value)
		elif typ=='quantity':
			if ' ' in value:
				vs = value.split()
				v = vs[0]
				unit = ' '.join(vs[1:])
			else:
				v = value
				unit = '1'
			value = ValueClass('quantity', float(v), unit)
		else:
			if '/' in value or ('-' in value and '-' != value[0]):
				split_char = '/' if '/' in value else '-'
				p1, p2 = value.find(split_char), value.rfind(split_char)
				y, m, d = int(value[:p1]), int(value[p1+1:p2]), int(value[p2+1:])
				value = ValueClass('date', date(y, m, d))
			else:
				value = ValueClass('year', int(value))
		return value



	def forward(self, program, inputs, 
				ignore_error=False, show_details=False):
		memory = []
		program = ['<START>'] + program + ['<END>']
		inputs = [[]] + inputs + [[]]
		try:
			# infer the dependency based on the function definition
			dependency = []
			branch_stack = []
			for i, p in enumerate(program):
				if p in {'<START>', '<END>', '<PAD>'}:
					dep = []
				elif p in {'FindAll', 'Find'}:
					dep = []
					branch_stack.append(i - 1)
				elif p in {'And', 'Or', 'SelectBetween', 'QueryRelation', 'QueryRelationQualifier'}:
					dep = [branch_stack[-1], i-1]
					branch_stack = branch_stack[:-1]
				else:
					dep = [i-1]
				dependency.append(dep)

			memory = []
			for p, dep, inp in zip(program, dependency, inputs):
				if p == 'What':
					p = 'QueryName'
				if p == '<START>':
					res = None
				elif p == '<END>':
					break
				else:
					fun_args = [memory[x] for x in dep]
					func = getattr(self, p)
					res = func(*fun_args, *inp)

				memory.append(res)
				if show_details:
					print(p, dep, inp)
					print(res)
			return [str(_) for _ in memory[-1]] if isinstance(memory[-1], list) else str(memory[-1])
		except Exception as e:
			if ignore_error:
				return None
			else:
				raise

	def FindAll(self):
		"""
		返回知识库中所有实体

		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个成员是None
		"""	
		entity_ids = list(self.kb.entities.keys())
		return (entity_ids, None)

	def Find(self, name):
		"""
		找出具有特定名字的所有实体

		Args:
			name (string): 实体的名字
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个成员是None
		"""
		entity_ids = self.kb.name_to_id[name]
		return (entity_ids, None)

	def FilterConcept(self, entities, concept_name):
		"""
		找出属于特定概念的所有实体

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			concept_name (string): 给定的概念标签
		
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是输入实体集合的交集，第二个成员是None
		"""
		entity_ids, _ = entities
		concept_ids = self.kb.name_to_id[concept_name]
		entity_ids_2 = []
		for i in concept_ids:
			entity_ids_2 += self.kb.concept_to_entity.get(i, [])
		entity_ids = list(set(entity_ids) & set(entity_ids_2))
		return (entity_ids, None)

	def _filter_attribute(self, entity_ids, tgt_key, tgt_value, op, typ):
		tgt_value = self._parse_key_value(tgt_key, tgt_value, typ)
		res_ids = []
		res_facts = []
		entity_ids = set(entity_ids) & set(self.kb.attribute_inv_index[tgt_key].keys())
		for ent_id in entity_ids:
			for idx in self.kb.attribute_inv_index[tgt_key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]			
				k, v = attr_info['key'], attr_info['value']
				if k==tgt_key and v.can_compare(tgt_value) and comp(v, tgt_value, op):
					res_ids.append(ent_id)
					res_facts.append(attr_info)
		return (res_ids, res_facts)

	def FilterStr(self, entities, key, value):
		"""
		针对字符串类型的属性，根据key和value筛选出满足该条件的所有实体，返回实体与对应的属性型三元组

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			key (string): 属性键
			value (string): 属性值
		
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表
		"""
		entity_ids, _ = entities
		op = '='
		return self._filter_attribute(entity_ids, key, value, op, 'string')

	def FilterNum(self, entities, key, value, op):
		"""
		针对数值类型的属性，key和value指定键值，op指定比较运算符，返回实体与对应的属性型三元组

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			key (string): 属性键
			value (string): 属性值，为数值类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个
		
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表
		"""
		entity_ids, _ = entities
		return self._filter_attribute(entity_ids, key, value, op, 'quantity')

	def FilterYear(self, entities, key, value, op):
		"""
		针对年份类型的属性，key和value指定键值，op指定比较运算符，返回实体与对应的属性型三元组

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			key (string): 属性键
			value (string): 属性值，为年份类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个
		
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表
		"""
		entity_ids, _ = entities
		return self._filter_attribute(entity_ids, key, value, op, 'year')

	def FilterDate(self, entities, key, value, op):
		"""
		针对日期类型的属性，key和value指定键值，op指定比较运算符，返回实体与对应的属性型三元组

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			key (string): 属性键
			value (string): 属性值，为日期类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个
		
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表
		"""
		entity_ids, _ = entities
		return self._filter_attribute(entity_ids, key, value, op, 'date')

	def _filter_qualifier(self, entity_ids, facts, tgt_key, tgt_value, op, typ):
		tgt_value = self._parse_key_value(tgt_key, tgt_value, typ)
		res_ids = []
		res_facts = []
		for i, f in zip(entity_ids, facts):
			for qk, qvs in f['qualifiers'].items():
				if qk == tgt_key:
					for qv in qvs:
						if qv.can_compare(tgt_value) and comp(qv, tgt_value, op):
							res_ids.append(i)
							res_facts.append(f)
							break
		return (res_ids, res_facts)

	def QFilterStr(self, entities, qkey, qvalue):
		"""
		使用修饰键qkey和修饰值qvalue对三元组进行过滤，筛选出符合条件的三元组与对应的实体

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			qkey (string): 修饰键
			qvalue (string): 修饰值，为字符串类型

		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表
		"""
		entity_ids, facts = entities
		op = '='
		return self._filter_qualifier(entity_ids, facts, qkey, qvalue, op, 'string')

	def QFilterNum(self, entities, qkey, qvalue, op):
		"""
		与 QFilterStr 类似，但针对数值类型的修饰值，op指定比较运算符

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			qkey (string): 修饰键
			qvalue (string): 修饰值，为数值类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表

		"""
		entity_ids, facts = entities
		return self._filter_qualifier(entity_ids, facts, qkey, qvalue, op, 'quantity')

	def QFilterYear(self, entities, qkey, qvalue, op):
		"""
		与 QFilterStr 类似，但针对数值类型的修饰值，op指定比较运算符

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			qkey (string): 修饰键
			qvalue (string): 修饰值，为年份类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表

		"""
		entity_ids, facts = entities
		return self._filter_qualifier(entity_ids, facts, qkey, qvalue, op, 'year')

	def QFilterDate(self, entities, qkey, qvalue, op):
		"""
		与 QFilterStr 类似，但针对数值类型的修饰值，op指定比较运算符

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是三元组列表
			qkey (string): 修饰键
			qvalue (string): 修饰值，为日期类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个
		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是实体列表，第二个是三元组列表

		"""
		entity_ids, facts = entities
		return self._filter_qualifier(entity_ids, facts, qkey, qvalue, op, 'date')

	def Relate(self, entities, relation, direction):
		"""
		找出与输入实体有特定关系的所有实体及对应的三元组

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个是None或三元组列表
			relation (string): 关系标签
			direction (string): "forward" 或者 "backward"，代表输入实体是关系的头实体或者尾实体

		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是与输入实体有特定关系的实体列表，第二个成员是对应的三元组列表
		"""
		entity_ids, _ = entities
		res_ids = []
		res_facts = []
		entity_ids = set(entity_ids) & set(self.kb.relation_inv_index[(relation,direction)].keys())
		for ent_id in entity_ids:
			for idx in self.kb.relation_inv_index[(relation,direction)][ent_id]:
				rel_info = self.kb.entities[ent_id]['relations'][idx]
				res_ids.append(rel_info['object'])
				res_facts.append(rel_info)
		return (res_ids, res_facts)

	def And(self, l_entities, r_entities):
		"""
		返回两个实体集合的交集

		Args:
			l_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			r_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表

		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是输入实体集合的交集，第二个成员是None

		"""
		entity_ids_1, _ = l_entities
		entity_ids_2, _ = r_entities
		return (list(set(entity_ids_1) & set(entity_ids_2)), None)

	def Or(self, l_entities, r_entities):
		"""
		返回两个实体集合的并集

		Args:
			l_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			r_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表

		Returns:
			:obj:`tuple`: 返回一个二元组，第一个成员是输入实体集合的并集，第二个成员是None

		"""
		entity_ids_1, _ = l_entities
		entity_ids_2, _ = r_entities
		return (list(set(entity_ids_1) | set(entity_ids_2)), None)

	def QueryName(self, entities):
		"""
		查询实体的名字

		Args:
			entities (tuple): 二元组，第一个成员是实体列表，第二个成员是None或者三元组列表

		Returns:
			:obj:`list`: 返回一个列表，每个元素是string，对应输入实体的名字
		"""
		entity_ids, _ = entities
		res = []
		for entity_id in entity_ids:
			name = self.kb.entities[entity_id]['name']
			res.append(name)
		return res

	def Count(self, entities):
		"""
		查询实体集合的数量

		Args：
			entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
		
		Returns:
			:obj:`int`: 返回输入实体列表的大小
		"""
		entity_ids, _ = entities
		return len(entity_ids)

	def SelectBetween(self, l_entities, r_entities, key, op):
		"""
		在两个实体中，查询特定属性值更大/更小的实体

		Args:
			l_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			r_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			key (string): 属性，要求其属性值为数值类型，如"height"
			op (string): 比较符，"less"或者"greater"，代表查询属性值更小或更大的实体

		Returns:
			:obj:`str`: 返回实体的名字

		"""
		entity_ids_1, _ = l_entities
		entity_ids_2, _ = r_entities
		candidates = []
		for ent_id in entity_ids_1:
			for idx in self.kb.attribute_inv_index[key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]
				candidates.append((ent_id, attr_info['value']))
		for ent_id in entity_ids_2:
			for idx in self.kb.attribute_inv_index[key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]
				candidates.append((ent_id, attr_info['value']))
		candidates = list(filter(lambda x: x[1].type=='quantity', candidates))
		unit_cnt = defaultdict(int)
		for x in candidates:
			unit_cnt[x[1].unit] += 1   
		common_unit = Counter(unit_cnt).most_common()[0][0]
		candidates = list(filter(lambda x: x[1].unit==common_unit, candidates))
		sort = sorted(candidates, key=lambda x: x[1])
		i = sort[0][0] if op=='less' else sort[-1][0]
		name = self.kb.entities[i]['name']
		return name

	def SelectAmong(self, entities, key, op):
		"""
		在一个实体集合中，查询特定属性值最大/最小的实体

		Args:
			entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			key (string): 属性，要求其属性值为数值类型，如"height"
			op (string): 比较符，"smallest"或者"largest"，代表查询属性值最小或最大的实体

		Returns:
			:obj:`list`: 返回实体名字列表，每个元素是string（可以有多个最大/最小值）

		"""
		entity_ids, _ = entities
		entity_ids = set(entity_ids)
		candidates = []
		for ent_id in entity_ids:
			for idx in self.kb.attribute_inv_index[key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]
				candidates.append((ent_id, attr_info['value']))
		candidates = list(filter(lambda x: x[1].type=='quantity', candidates))
		unit_cnt = defaultdict(int)
		for x in candidates:
			unit_cnt[x[1].unit] += 1
		common_unit = Counter(unit_cnt).most_common()[0][0]
		candidates = list(filter(lambda x: x[1].unit==common_unit, candidates))
		sort = sorted(candidates, key=lambda x: x[1])
		value = sort[0][1] if op=='smallest' else sort[-1][1]
		names = list(set([self.kb.entities[i]['name'] for i,v in candidates if v==value])) # 可以有多个最大/最小值
		return names

	def QueryAttr(self, entities, key):
		"""
		查询实体的特定属性值

		Args:
			entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			key (string): 属性
		
		Returns:
			:obj:`list`: 返回属性值列表，每个元素是string，是对应实体指定属性的属性值
		"""
		entity_ids, _ = entities
		res = []
		for ent_id in entity_ids:
			for idx in self.kb.attribute_inv_index[key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]
				res.append(attr_info['value'])
		return res

	def QueryAttrUnderCondition(self, entities, key, qkey, qvalue):
		"""
		返回输入实体在特定修饰条件下的属性值

		Args:
			entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			key (string): 属性键
			qkey (string): 修饰键
			qvalue (string): 修饰值
		
		Returns:
			:obj:`list`: 返回满足条件的属性值列表，每个属性值是 ValueClass
		"""
		entity_ids, _ = entities
		qvalue = self._parse_key_value(qkey, qvalue)
		res = []
		for ent_id in entity_ids:
			for idx in self.kb.attribute_inv_index[key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]
				flag = False
				for qk, qvs in attr_info['qualifiers'].items():
					if qk == qkey:
						for qv in qvs:
							if qv.can_compare(qvalue) and comp(qv, qvalue, "="):
								flag = True
								break
					if flag:
						break
				if flag:
					v = attr_info['value']
					res.append(v)
		return res

	def _verify(self, s_value, t_value, op, typ):
		attr_values = s_value
		value = self._parse_key_value(None, t_value, typ)
		match = []
		for attr_value in attr_values:
			if attr_value.can_compare(value) and comp(attr_value, value, op):
				match.append(1)
			else:
				match.append(0)
		if sum(match) >= 1 and sum(match) == len(match):
			answer = 'yes'
		elif sum(match) == 0:
			answer = 'no'
		else:
			answer = 'not sure'
		return answer

	def VerifyStr(self, s_value, t_value):
		"""
		验证 QueryAttr 或 QueryAttrUnderCondition 函数的输出是否等于给定的字符串

		Args:
			s_value (list): 一个 ValueClass 实例列表，为 QueryAttr 或 QueryAttrUnderCondition 函数的输出
			t_value (string): 给定的属性值，为字符串类型
		
		Returns:
			:obj:`string`: "yes", 或 "no" 或 "not sure" 代表属性值与给定的字符串相同，不同，或不确定
		"""
		op = '='
		return self._verify(s_value, t_value, op, 'string')
		
	def VerifyNum(self, s_value, t_value, op):
		"""
		与 VerifyStr 类似，但针对数值类型，验证属性值是否满足特定条件，Op指定比较运算符

		Args:
			s_value (list): 一个 ValueClass 实例列表，为 QueryAttr 或 QueryAttrUnderCondition 函数的输出
			t_value (string): 给定的属性值, 为数值类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个

		
		Returns:
			:obj:`string`: "yes", 或 "no" 或 "not sure" 代表属性值与给定的字符串相同，不同，或不确定
		"""
		return self._verify(s_value, t_value, op, 'quantity')

	def VerifyYear(self, s_value, t_value, op,):
		"""
		与 VerifyStr 类似，但针对年份类型

		Args:
			s_value (list): 一个 ValueClass 实例列表，为 QueryAttr 或 QueryAttrUnderCondition 函数的输出
			t_value (string): 给定的属性值, 为年份类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个

		
		Returns:
			:obj:`string`: "yes", 或 "no" 或 "not sure" 代表属性值与给定的字符串相同，不同，或不确定

		"""
		return self._verify(s_value, t_value, op, 'year')

	def VerifyDate(self, s_value, t_value, op,):
		"""s
		与 VerifyStr 类似，但针对日期类型

		Args:
			s_value (list): 一个 ValueClass 实例列表，为 QueryAttr 或 QueryAttrUnderCondition 函数的输出
			t_value (string): 给定的属性值, 为日期类型
			op (string): 比较运算符，"=", "!=", "<", ">"中的一个

		
		Returns:
			:obj:`string`: "yes", 或 "no" 或 "not sure" 代表属性值与给定的字符串相同，不同，或不确定

		"""        
		return self._verify(s_value, t_value, op, 'date')

	def QueryRelation(self, s_entities, t_entities):
		"""
		查询实体之间的关系

		Args:
			s_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			t_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表

		Returns:
			:obj:`list`: 返回关系列表，每个关系是string
		"""
		entity_ids_1, _ = s_entities
		entity_ids_2, _ = t_entities
		res = []
		for entity_id_1 in entity_ids_1:
			for entity_id_2 in entity_ids_2:
				for idx in self.kb.forward_relation_index[(entity_id_1, entity_id_2)]:
					rel_info = self.kb.entities[entity_id_1]['relations'][idx]
					res.append(rel_info['relation'])
		return res

	def QueryAttrQualifier(self, entities, key, value, qkey):
		"""
		查询给定实体某个属性的特定修饰值

		Args:
			entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			key (string): 属性标签
			value (string): 属性值
			qkey (string): 修饰符标签
		
		Returns:
			:obj:`list`: 返回修饰值列表，每个修饰值是string
		"""
		entity_ids, _ = entities
		value = self._parse_key_value(key, value)
		res = []
		for ent_id in entity_ids:
			for idx in self.kb.attribute_inv_index[key][ent_id]:
				attr_info = self.kb.entities[ent_id]['attributes'][idx]
				if attr_info['key']==key and attr_info['value'].can_compare(value) and \
					comp(attr_info['value'], value, '='):
					for qk, qvs in attr_info['qualifiers'].items():
						if qk == qkey:
							res += qvs
		return res

	def QueryRelationQualifier(self, s_entities, t_entities, relation, qkey):
		"""
		查询给定实体之间关系三元组的特定修饰值

		Args:
			s_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			t_entities (tuple): 二元组，第一个成员是一个实体列表，第二个成员是None或者三元组列表
			relation (string): 关系标签
			qkey (string): 修饰符标签
		
		Returns:
			:obj:`list`: 返回修饰值列表，每个修饰值是string
		"""
		entity_ids_1, _ = s_entities
		entity_ids_2, _ = t_entities
		res = []
		for entity_id_1 in entity_ids_1:
			for entity_id_2 in entity_ids_2:
				for idx in self.kb.forward_relation_index[(entity_id_1, entity_id_2)]:
					rel_info = self.kb.entities[entity_id_1]['relations'][idx]
					if rel_info['relation']==relation:
						for qk, qvs in rel_info['qualifiers'].items():
							if qk == qkey:
								res += qvs
		return res