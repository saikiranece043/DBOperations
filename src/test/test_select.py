import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from src.select import column_offset_validation
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



