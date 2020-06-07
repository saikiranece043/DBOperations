from applycond import apply_logicalop,apply_condition



def run1_query_tree(tree,line, arguments):
    '''
    Returns a boolean after applying the query tree on the input line
    :param tree: Query  tree
    :param line: line read from the input data file
    :return: applies conditional operators to return a Boolean
    '''

    if type(tree) == tuple:
        root, lefttree, righttree = tree

    #root = root.lower()

    if root != 'and' and root!= 'or' and root!= 'not':
        #print(f'Performing select operation ({root},{lefttree},{righttree})')
        eval = apply_condition((root, lefttree, righttree), line, arguments)
        #print(f'Performed select operation ({root},{lefttree},{righttree}):: eval {eval}')
        return eval

    #evaluate left tree

    left_value = run1_query_tree(lefttree,line,arguments)


    #evaluate right tree

    #Pruning the Query Tree to minimize the operations
    if root == 'and' and left_value == False:
        right_value = left_value
    elif root == 'or' and left_value == True:
        right_value = left_value
    else:
        right_value =  run1_query_tree(righttree,line,arguments)
    #print("performing select operation",right_value)

    logicaleval = apply_logicalop(root, left_value, right_value)
    #print(f'{lefttree} {root} {righttree}::{left_value} {root} {right_value}:: finaleval {logicaleval}')
    return logicaleval


