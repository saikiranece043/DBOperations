import pytest
from src.parse_cond import parsecondition


@pytest.mark.parametrize("grammar, tree", [
    ('#1 > 2',('>', '#1', 2)),
    ('#2 == "teststring"', ('==', '#2', 'teststring')),
    ('#id >  2', ('>', '#id', 2)),
    ('#name ==  "test"', ('==', '#name', 'test')),
    ('#1 > 2 and #2 == "test"',  ('and', ('>', '#1', 2), ('==', '#2', 'test'))),
    ('#name == "test" and #id >= 5', ('and', ('==', '#name', 'test'), ('>=', '#id', 5))),
    ('#1 > 2 and ( #2 >= 5 and #2 == "test" )', ('and', ('>', '#1', 2), ('and', ('>=', '#2', 5), ('==', '#2', 'test')))),
    ('( #2 >= 5 and #2 == "test" ) and #1 > 2', ('and', ('and', ('>=', '#2', 5), ('==', '#2', 'test')), ('>', '#1', 2))),
    ('(#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 == "test" )', ('and', ('or', ('>', '#1', 2), ('>=', '#5', 6)), ('and', ('>=', '#2', 5), ('==', '#2', 'test')))),
    ('((#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 == "test" )) and #1 > 2', ('and', ('and', ('or', ('>', '#1', 2), ('>=', '#5', 6)), ('and', ('>=', '#2', 5), ('==', '#2', 'test'))), ('>', '#1', 2)) )

])
def test_grammar(grammar, tree):
    '''
    This function is to test the tree generated for a given grammar
    Several common grammar terminologies are tested against the expected output
    :param grammar: input
    :param tree: expected output
    :return:
    '''
    assert tree == parsecondition(grammar)


