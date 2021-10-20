import unittest
from kopl.kopl import KoPLEngine
from kopl.util import *
import copy

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

engine = KoPLEngine(copy.deepcopy(example_kb))

class TestExample(unittest.TestCase):
    def test_Find(self):
        ans = engine.Find('LeBron James Jr.')
        self.assertTrue(isinstance(ans, tuple))
        self.assertTrue(isinstance(ans[0], list))
        self.assertTrue(len(ans[0]), 1)
    
    def test_Relate(self):
        ans = engine.QueryName(
            engine.Relate(
            entities = engine.Find('LeBron James Jr.'),
            relation = 'father',
            direction = 'forward'
            )
        )
        self.assertEqual(ans[0], 'LeBron James')

    def test_SelectBetween(self):
        ans = engine.SelectBetween(
            engine.Find('LeBron James Jr.'),
            engine.Relate(
                engine.Find('LeBron James Jr.'),
                relation = 'father',
                direction = 'forward'
            ),
            key = 'height',
            op = 'greater'
        )
        self.assertEqual(ans, 'LeBron James')
    
    def test_SelectAmong(self):
        ans = engine.SelectAmong(
            engine.Or(
                engine.Find('LeBron James'),
                engine.Find('LeBron James Jr.')
            ),
            key = 'height',
            op = 'largest'
        )
        self.assertEqual(ans, ['LeBron James'])

    def test_QueryAttr(self):
        ans = engine.QueryAttr(
            entities = engine.Find('LeBron James'),
            key = 'height'
        )
        self.assertTrue(ans[0].can_compare(ValueClass('quantity', 206, 'centimetre')))
        self.assertTrue(comp(ans[0], ValueClass('quantity', 206, 'centimetre'), '='))

    def test_QueryRelationQualifier(self):
        ans = engine.QueryRelationQualifier(
            s_entities = engine.Find('LeBron James'),
            t_entities = engine.Find('Cleveland Cavaliers'),
            relation = 'drafted by',
            qkey = 'point in time'
        )    
        self.assertEqual(str(ans[0]), '2003-06-26')

    def test_QueryAttrQualifier(self):
        ans = engine.QueryAttrQualifier(
            entities = engine.Find('Akron'),
            key = 'population',
            value = '199110',
            qkey = 'point in time'
        )
        self.assertTrue(ans[0].can_compare(ValueClass('year', 2010)))
        self.assertTrue(comp(ans[0], ValueClass('year', 2010), '='))

    def test_QueryAttrUnderCondition(self):
        ans = engine.QueryAttrUnderCondition(
            entities = engine.Find('Akron'),
            key = 'population',
            qkey = 'point in time',
            qvalue = '2010'
        )
        self.assertTrue(ans[0].can_compare(ValueClass('quantity', 199110, '1')))
        self.assertTrue(comp(ans[0], ValueClass('quantity', 199110, '1'), '='))
    
    def test_FilterConcept(self):
        ans = engine.FilterConcept(
            entities = engine.Find('Cleveland Cavaliers'),
            concept_name = 'basketball player'
        )
        self.assertEqual(ans[0], [])
        ans = engine.FilterConcept(
            entities = engine.Find('Cleveland Cavaliers'),
            concept_name = 'basketball team'
        )
        self.assertEqual(ans[0], ['Q162990'])
    
    def test_FilterNum(self):
        ans = engine.FilterNum(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            ),
            key = 'height',
            value = '188 centimetre',
            op = '>'
        )
        self.assertEqual(engine.QueryName(ans)[0], 'LeBron James')
        ans = engine.FilterNum(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            ),
            key = 'height',
            value = '180 centimetre',
            op = '>'
        )
        self.assertEqual(len(ans[0]), 2)
    
    def test_FilterStr(self):
        ans = engine.FilterStr(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            ),
            key = 'sex or gender',
            value = 'male',
        )
        self.assertEqual(len(engine.QueryName(ans)), 2)
        self.assertTrue('LeBron James' in engine.QueryName(ans))
        self.assertTrue('LeBron James Jr.' in engine.QueryName(ans))

    def test_FilterYear(self):
        ans = engine.FilterYear(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            ),
            key = 'work period (start)',
            value = '2003',
            op = '='
        )
        self.assertEqual(engine.QueryName(ans), ['LeBron James'])
        ans = engine.FilterYear(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            ),
            key = 'work period (start)',
            value = '2000',
            op = '='
        )
        self.assertEqual(engine.QueryName(ans), [])
    
    def test_FilterDate(self):
        ans = engine.FilterDate(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            ),
            key = 'date of birth',
            value = '1984-12-30',
            op = '='
        )
        self.assertEqual(engine.QueryName(ans), ['LeBron James'])
    
    def test_QFilterDate(self):
        ans = engine.QFilterDate(
            entities = engine.Relate(
                entities = engine.Find('LeBron James'),
                relation = 'drafted by',
                direction = 'forward'
            ),
            qkey = 'point in time',
            qvalue = '2003-06-26',
            op = '='
        )
        self.assertEqual(engine.QueryName(ans)[0], 'Cleveland Cavaliers')
    
    def test_QFilterYear(self):
        ans = engine.QFilterYear(
            entities = engine.Relate(
                entities = engine.Find('LeBron James'),
                relation = 'drafted by',
                direction = 'forward'
            ),
            qkey = 'point in time',
            qvalue = '2003',
            op = '='
        )
        self.assertEqual(engine.QueryName(ans)[0], 'Cleveland Cavaliers')
    
    def test_QFilterStr(self):
        ans = engine.QFilterStr(
            entities = engine.Relate(
                entities = engine.Find('LeBron James'),
                relation = 'member of sports team',
                direction = 'forward'
            ),
            qkey = 'position played on team/speciality',
            qvalue = 'small forward',
        )
        self.assertEqual(engine.QueryName(ans)[0], 'Cleveland Cavaliers')
    
    def test_QFilterNum(self):
        ans = engine.QFilterNum(
            entities = engine.Relate(
                entities = engine.Find('LeBron James'),
                relation = 'member of sports team',
                direction = 'forward'
            ),
            qkey = 'sport number',
            qvalue = '23',
            op = '='
        )
        self.assertEqual(engine.QueryName(ans)[0], 'Cleveland Cavaliers')
    
    def test_Count(self):
        ans = engine.Count(
            entities = engine.FilterConcept(
                entities = engine.FindAll(),
                concept_name = 'basketball player'
            )
        )
        self.assertEqual(ans, 2)
    
    def test_VerifyStr(self):
        ans = engine.VerifyStr(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'sex or gender'
            ),
            t_value = 'male'
        )
        self.assertEqual(ans, 'yes')
        ans = engine.VerifyStr(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'sex or gender'
            ),
            t_value = 'female'
        )
        self.assertEqual(ans, 'no')

    def test_VerifyNum(self):
        ans = engine.VerifyNum(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'height'
            ),
            t_value = '206 centimetre',
            op = '='
        )
        self.assertEqual(ans, 'yes')
        ans = engine.VerifyNum(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'height'
            ),
            t_value = '208 centimetre',
            op = '='
        )
        self.assertEqual(ans, 'no')
    
    def test_VerifyDate(self):
        ans = engine.VerifyDate(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'date of birth'
            ),
            t_value = '1984-12-30',
            op = '='
        )
        self.assertEqual(ans, 'yes')
        ans = engine.VerifyDate(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'date of birth'
            ),
            t_value = '1983-12-30',
            op = '='
        )
        self.assertEqual(ans, 'no')

    def test_VerifyYear(self):
        ans = engine.VerifyYear(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'date of birth'
            ),
            t_value = '1984',
            op = '='
        )
        self.assertEqual(ans, 'yes')
        ans = engine.VerifyYear(
            s_value = engine.QueryAttr(
                entities = engine.Find('LeBron James'),
                key = 'date of birth'
            ),
            t_value = '1983',
            op = '='
        )
        self.assertEqual(ans, 'no')
    
    def test_QueryRelation(self):
        ans = engine.QueryRelation(
            s_entities = engine.Find('LeBron James Jr.'),
            t_entities = engine.Find('LeBron James')
        )
        self.assertEqual(ans, ['father'])
        
def run_test():
    unittest.main()

