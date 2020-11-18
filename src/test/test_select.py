import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from src.select import column_offset_validation, myselect, parsecondition
import pytest


@pytest.mark.parametrize(("inputargs, outputargs"),[
 (['#20 == 1',open('./src/test/test.csv'), sys.stdout, False, '|', None],'The column offset "#20" should be in the range (0, 15)'),
 (['#test == 1',open('./src/test/test.csv'), sys.stdout, False, '|', None],'column offset "#test" cannot be a string as input data has no header'),
 (['#test == 1',open('./src/test/test.csv'), sys.stdout, True, '|', None], 'column offset "#test" entered is not found in input data header'),
 (['#2 == 1',open('./src/test/test.csv'), sys.stdout, True, ',', None], 'Did you miss passing delimiter arg?')

])
def test_col_validation_negative(inputargs, outputargs):
    '''
	All Negative validation scenarios are tested
	:return:
	'''
    with pytest.raises(Exception) as excinfo:
        column_offset_validation(inputargs)
    assert str(excinfo.value) == outputargs


def test_col_validation_positive():
    inputargs = ['#1 == 3',open('./src/test/test.csv'), sys.stdout, False, '|', None]
    expectedout = '1|310379|15395|1|17|23619.12|0.04|0.02|N|O|1996-03-13|1996-02-12|1996-03-22|DELIVER IN PERSON|TRUCK|egular courts above the\n'
    assert expectedout == column_offset_validation(inputargs)
    inputargs[1].close()


def test_select_main():
    inputargs = [('>', '#1', 2),
                 open('./src/test/test.csv'),
                 open('./src/test/result.csv','w+'), False, '|', None]
    firstline = '1|310379|15395|1|17|23619.12|0.04|0.02|N|O|1996-03-13|1996-02-12|1996-03-22|DELIVER IN PERSON|TRUCK|egular courts above the'
    expectedout = '3|8594|3595|1|45|67616.55|0.06|0.00|R|F|1994-02-02|1994-01-04|1994-02-23|NONE|AIR|ongside of the furiously brave acco'
    myselect(inputargs, firstline)
    for x in inputargs[2]:
        assert expectedout == x
    inputargs[1].close()
    inputargs[2].close()
    os.remove('./src/test/result.csv')
