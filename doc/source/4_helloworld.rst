The first KoPL program
====================================



Knowledge Base Preparation
----------------------------------

Currently, we support knowledge base in JSON format in the form of:

::

	{
		# Concepts
		'concepts': {
			'id': {
				'name': '',
				'subclassOf': ['<concept_id>'],
			}
		},
		# Entities, which do not coincide with concepts
		'entities': {
			'id': {
				'name': '<entity_name>',
				'instanceOf': ['<concept_id>'],
				'attributes': [ 
					{
						'key': '<key>',
						'value': {
							'type': 'string'/'quantity'/'date'/'year'
							'value':  # The type of quantity is float or int, the type of year  is int, the type of date is 'yyyy/mm/dd'
							'unit':   # It is used for quantity, the type of it is str. For example, the unit of 'height' can be 'centimetre' and the unit of 'population' can be '1'. 
						},
						'qualifiers': {
							'<qk>': [
								<qv>, # Every qv is a dictionary like 'value', including 'type', 'value' and 'int'.
							]
						}
					}
				]
				'relations': [ 
					{
						'relation': '<relation>',
						'direction': 'forward' or 'backward',
						'object': '<object_id>',
						'qualifiers': {
							'<qk>': [
								<qv>, # Every qv is a dictionary like 'value', including 'type', 'value' and 'int'.
							]
						}
					}
				]
			}
		}
	}

.. image:: knowledge_element.jpg
  :width: 600
  :alt: Alternative text

For example, for the knowledge base above, it is represented as

::

	example_kb = {
		'concepts': {
			'Q13393265': {
				'name': 'basketball team',
				'subclassOf': ['Q12973014'] 
			},
			'Q12973014': {
				'name': 'sports team',
				'subclassOf': []
			},
			'Q3665646': {
				'name': 'basketball player',
				'subclassOf': ['Q2066131']
			},
			'Q2066131': {
				'name': 'athlete',
				'subclassOf': []
			}
		},
		'entities': {
			'Q36159': {
				'name': 'LeBron James',
				'instanceOf': ['Q3665646'],
				'attributes': [
					{
						'key': 'height',
						'value': {
							'type': 'quantity',
							'value': 206,
							'unit': 'centimetre'
						},
						'qualifiers': {}
					},
					{
						'key': 'work period (start)',
						'value': {
							'type': 'year',
							'value': 2003
						},
						'qualifiers': {}
					},
					{
						'key': 'sex or gender',
						'value': {
							'type': 'string',
							'value': 'male'
						},
						'qualifiers': {}
					},
					{
						'key': 'date of birth',
						'value': {
							'type': 'date',
							'value': '1984-12-30'
						},
						'qualifiers': {}
					}
				],
				'relations': [
					{
						'relation': 'place of birth',
						'direction': 'forward',
						'object': 'Q163132',
						'qualifiers': {}
					}, 
					{
						'relation': 'drafted by',
						'direction': 'forward',
						'object': 'Q162990',
						'qualifiers': {
							'point in time': [
								{
									'type': 'date',
									'value': '2003-06-26'
								}
							]
						}
					},
					{
						'relation': 'child',
						'direction': 'forward',
						'object': 'Q22302425',
						'qualifiers': {}

					},
					{
						'relation': 'member of sports team',
						'direction': 'forward',
						'object': 'Q162990',
						'qualifiers': {
							'position played on team/speciality': [
								{
									'type': 'string',
									'value': 'small forward'
								}
							],
							'sport number': [
								{
									'type': 'quantity',
									'value': 23,
									'unit': '1'
								}
							]
						}
					}
				]
			},
			'Q163132': {
				'name': 'Akron',
				'instanceOf': [],
				'attributes': [
					{
						'key': 'population',
						'value': {
							'type': 'quantity',
							'value': 199110,
							'unit': '1'
						},
						'qualifiers': {
							'point in time': [
								{
									'type': 'year',
									'value': 2010
								}
							]
						}
					}
				],
				'relations': []
			},
			'Q162990': {
				'name': 'Cleveland Cavaliers',
				'instanceOf': ['Q13393265'],
				'attributes': [
					{
						'key': 'inception',
						'value': {
								'type': 'year',
								'value': 1970
						},
						'qualifiers': {}
					}
				],
				'relations': []
			},
			'Q22302425': {
				'name': 'LeBron James Jr.',
				'instanceOf': ['Q3665646'],
				'attributes': [
					{
						'key': 'height',
						'value': {
							'type': 'quantity',
							'value': 188,
							'unit': 'centimetre'
						},
						'qualifiers': {} 
					},
					{
						'key': 'sex or gender',
						'value': {
							'type': 'string',
							'value': 'male'
						},
						'qualifiers': {}
					},
					{
						'key': 'date of birth',
						'value': {
							'type': 'date',
							'value': '2004-10-06'
						},
						'qualifiers': {}
					}
				],
				'relations': [
					{
						'relation': 'father',
						'direction': 'forward',
						'object': 'Q36159',
						'qualifiers': {}
					}
				]

			}
		}

	}


KBQA based on KoPL
----------------------------

KoPL is implemented in Python. We only give an example here. Please refer to :doc:`the page of apis  <7_kopl>` for more information. Besides, please ref to :doc:`the page of knowledge operators <2_function>` for an introduction to the basic functions of KoPL.

::

	from kopl.kopl import KoPLEngine
	from kopl.test.test_example import example_kb

	engine = KoPLEngine(example_kb)

	ans = engine.SelectBetween(
		engine.Find('LeBron James Jr.'),
		engine.Relate(
			engine.Find('LeBron James Jr.'),
			'father',
			'forward'
		),
		'height',
		'greater'
	)

	print(ans)

In this example, we look up who is taller, LeBron James Jr. or his father, and the KoPL program gives us the correct answer: LeBron James!


See :doc:`the example page <5_example>` for more KoPL examples.

