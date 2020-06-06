
from src.parse_cond import parsecondition


g_testcases = [
    "#1 > 2",
    '#2 = "teststring"',
    '#id >  2',
    '#name =  "test"',
    '#1 > 2 and #2 = "test"',
    '#name = "test" and #id >= 5',
    '#1 > 2 and ( #2 >= 5 and #2 = "test" )',
    '( #2 >= 5 and #2 = "test" ) and #1 > 2',
    '(#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 = "test" )',
    '((#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 = "test" )) and #1 > 2'
]

g_testresp = [
('>', '#1', 2),
('=', '#2', '"teststring"'),
('>', '#id', 2),
('=', '#name', '"test"'),
('and', ('>', '#1', 2), ('=', '#2', '"test"')),
('and', ('=', '#name', '"test"'), ('>=', '#id', 5)),
('and', ('>', '#1', 2), ('and', ('>=', '#2', 5), ('=', '#2', '"test"'))),
('and', ('and', ('>=', '#2', 5), ('=', '#2', '"test"')), ('>', '#1', 2)),
('and', ('or', ('>', '#1', 2), ('>=', '#5', 6)), ('and', ('>=', '#2', 5), ('=', '#2', '"test"'))),
('and', ('and', ('or', ('>', '#1', 2), ('>=', '#5', 6)), ('and', ('>=', '#2', 5), ('=', '#2', '"test"'))), ('>', '#1', 2))
]



class TestParsecond:

    def test_simpleexpression(self):
        assert g_testresp[0] == parsecondition(g_testcases[0])

    def test_complexexpression(self):
        assert g_testresp[6] == parsecondition(g_testcases[6])

    def test_nestedexpression(self):
        assert g_testresp[8] == parsecondition(g_testcases[8])

    def test_compnestedexpression(self):
        assert g_testresp[9] == parsecondition(g_testcases[9])