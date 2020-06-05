import apply_cond
import sys
import timeit


def run1_query_tree(tree,line):
    '''
    Returns a boolean after applying the query tree on the input line
    :param tree: Query  tree
    :param line: line read from the input data file
    :return: applies conditional operators to return a Boolean
    '''

    if type(tree) == tuple:
        root, lefttree, righttree = tree


    if root!= 'and' and root!= 'or' and root!= 'not':
        #print(f'Performing select operation ({root},{lefttree},{righttree})')
        eval = apply_cond.apply_condition((root, lefttree, righttree), line)
        #print(f'Performed select operation ({root},{lefttree},{righttree}):: eval {eval}')
        return eval

    #evaluate left tree

    left_value = run1_query_tree(lefttree,line)
    #print("peforming select operation ",left_value)
    #evaluate right tree

    #Pruning the Query Tree to minimize the operations
    if root == 'and' and left_value == False:
        right_value = left_value
    else:
        right_value =  run1_query_tree(righttree,line)
    #print("performing select operation",right_value)

    logicaleval = apply_cond.apply_logicalop(root, left_value, right_value)
    #print(f'{lefttree} {root} {righttree}::{left_value} {root} {right_value}:: finaleval {logicaleval}')
    return logicaleval


query3 = ('and', ('and', ('or', ('>', '#20', 40), ('>=', '#5', 6)), ('and', ('>=', '#2', 5), ('=', '#2', '"test"'))), ('>', '#1', 2))
query = ('and',('>','#1','3'),('>=','#4','5'))
query1 = ('and',('>','#1','3'),('and' ,('>','#4','5'),('>','#6','2')) )
query_lineitems = ('and',('==','#9','"N"'),('and' ,('==','#15','"RAIL"'),('==','#14','"DELIVER IN PERSON"')) )


#print(run1_query_tree(query3))

'''
1|310379|15395|1|17|23619.12|0.04|0.02|N|O|1996-03-13|1996-02-12|1996-03-22|DELIVER IN PERSON|TRUCK|egular courts above the
1|Supplier#000000001| N kD4on9OM Ipw3,gf0JBoQDd7tgrzrddZ|17|27-918-335-1736|5755.94|each slyly above the careful

'''

def projection(line,columnsToProject=[1,2,3]):
    """
    The function takes a row and returns a modified row with required columns data
    :param line:
    :param columnsToProject:
    :return: user interested columns data separated by a separator
    """
    rowdata = line.split('|')
    return "|".join([rowdata[columnNumber-1] for columnNumber in columnsToProject])


def readfile():
    try:
        file = open('../resources/lineitem.csv', 'r')
        for line in file.readlines():
                eval = run1_query_tree(query_lineitems,line)
                if eval:
                    print(line)
    except OSError:
        print("error reading the file")
    finally:
        file.close()


#time taken to execute the program 138.774661164
# start = timeit.default_timer()
# readfile()
# end = timeit.default_timer()
# print(f'time taken to execute the program {end - start}')