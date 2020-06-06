import re

def get_type(op):
    '''
    Handles type conversion (all columns are read as strings)
    Supports conversion to int, float, string
    :param op: input is plain string
    :return: returns input with appropriate type conversion
    '''
    if op.isdecimal():
        return int(op)
    else:
        if re.match(r'\d+\.\d+',op):
            return float(op)
        else:
            return op
        # try:
        #     return float(op)
        # except:
        #     return op


def myeval(op, line, arguments):
    '''
    Extracts the column value from the line, converts column value and constant into appropriate python types
    :param op: op can be column reference or constant
    :param line: line read from the input data file
    :return: column and constant converted into appropriate types
    '''
    fields = line.split(arguments[4])
    index = op[1:]
    # if a column is referred by a number
    if index.isdecimal():
       index = int(index)
       cvalue = fields[index - 1]
       return get_type(cvalue)
    # if a column is referred by its name
    else:
        cvalue = fields[arguments[5][index]]
        return get_type(cvalue)



def apply_condition(condition, line, arguments):
    '''
    Returns evaluation of a condition on a line from the input data file
    :param condition: condition to apply on the operands
    :param line: line read from the input data file
    :return: True or False
    '''
    if (condition[0] == '>'):
        return (myeval(condition[1], line, arguments) > condition[2])
    elif (condition[0] == '<'):
        return (myeval(condition[1], line, arguments) < condition[2])
    elif (condition[0] == '<='):
        return (myeval(condition[1], line, arguments) <= condition[2])
    elif (condition[0] == '>='):
        return (myeval(condition[1], line, arguments) >= condition[2])
    elif (condition[0] == '=='):
        #print(myeval(condition[1],line),myeval(condition[2],line))
        return (myeval(condition[1], line, arguments) == condition[2])
    elif (condition[0] == '!='):
        return (myeval(condition[1], line, arguments) != condition[2])
    else:
        print("wrong or unallowed operator!")
        exit(-1)


def apply_logicalop(condition,op1,op2=None):
    '''
    Evaluates Logical Operation between two logical inputs
    :param condition:
    :param op1: Boolean
    :param op2: Optional Boolean
    :return: returns evaluation of op1,op2 as Boolean
    '''
    if condition == 'and':
         return op2 if op1 else False
    elif condition == "or":
         return True if op1 else op2
    elif condition == 'not':
        return not (op1)
    else:
        print("something wrong with the condition you passed")

