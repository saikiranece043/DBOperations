#!/usr/bin/env pypy
import sys
import argparse
from qtreeproc import run1_query_tree
from parse_cond import parsecondition


"""
user_interface uses argparse to get arguments from command line 
https://docs.python.org/2/library/argparse.html*/
as parsing proceeds, add results to resultlist in a fixed order.
First, the condition (since it's the only required argument)
second the input file (null if none given), third the output file (null if none given), finally a switch to indicate if the input file has a header.
"""


# return is a list resultlist with
# resultlist[0] = the condition (always present)
# resultlist[1] = input file name, if given; None if not.
# resultlist[2] = output file name, if given; None if not.
# resultlist[3] = boolean indicating whether a header exists in input
# resultlist[4] = line separator, if given; ',' if not

def user_interface():
    resultlist = []
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-c", "--condition", help="condition", required=True)
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-h", "--header", default=False, action="store_true", help="whether input file has header")
    parser.add_argument("-s", "--split", default=',', help="line separator")
    args = parser.parse_args()
    resultlist.append(args.condition)
    resultlist.append(args.input)
    resultlist.append(args.output)
    resultlist.append(args.header)
    resultlist.append(args.split)
    return resultlist





def column_offset_validation(arguments):
    """
    This function is to validate the column offset and return user friendly errors
    :return: void
    """
    inputfile = arguments[1]
    header = inputfile.readline()
    splitter = arguments[4]
    attributesCount = len(header.split(splitter))
    operands = arguments[0].split()

    if arguments[3]:
        for operand in operands:
            if operand.startswith('#'):
                #if you are here the column offset can be a integer or string
                if operand[1:].isdecimal():
                    data_error_handler(operand[1:],attributesCount)
                else:
                    # This block of code is executed for float or string
                    if operand[1:] not in header:
                        print(f'column reference {operand} entered is incorrect')
                        sys.exit(1)

    else:
        for operand in operands:
            if operand.startswith('#'):
                if operand[1:].isdecimal():
                    data_error_handler(operand,attributesCount)
                else:
                    print(f'column reference {operand} cannot be a string, perhaps you forgot to pass "-h" arg')
                    sys.exit(1)



def data_error_handler(data,attributesCount):
    """
    Function performs validation of the input data
    Checks if the data is string or integer
    If the data is integer it further checks if it's contained within a range
    :param data:
    :param range:
    :return: void
    """
    # if you are here that means the column offset should always be an integer

    if not data[1:].isdecimal():
        print(f'The column offset {data} should be an integer')
        sys.exit(1)
    # the column offset should be between 0...(attributesCount - 1)
    if int(data[1:]) not in range(0,attributesCount):
        print(f'The column offset {data} should be in the range (0, {attributesCount - 1 }) ')
        sys.exit(1)


"""
parse_condition receives a string with the first argument from user interface, breaks it down into components, 
checks that it's a well-formed condition, returns them in a list. 
In the list the operator always comes first, and the two operands later. 
For instance, "#3 > 5" becomes [">", '#3', 5] Complex conditions are parsed recursively:
"#3 > 5 and #2 == 5" becomes ["AND", [">", '#3', 5], ["==", '#2', 5]]
This recursive structure makes evaluation easy.
"""


def parse_condition(cond):
    OPERATORS = ['>','<','=' ,'>=','<=']
    condition = []
    cond = "".join([w and w + " " for w in cond.split()])
    # processing the condition. Error checking here.
    #print(cond)
    list = cond.split()
    #print(list)
    if ("AND" in list or "OR" in list):
        #print("complex condition parsing here")
        exit(0)
    condition.append(list[1])
    condition.append(list[0])
    #condition.append(list[2])
    #print(condition)
    return condition


"""
arguments[1] is the name of an input file or None. To get a file descriptor, the file is open; if None, standard input is used. This way, the rest of the program works with a file descriptor regardless of where the data comes from.
Similarly for output. This allows working with pipes.
"""


def set_input_output(arguments):
    if (arguments[1]):
        try:
            infile = open(arguments[1])
        except IOError:
            print('There was an error opening the input file!')
            exit(-1);
    else:
        infile = sys.stdin
    arguments[1] = infile
    if (arguments[2]):
        try:
            outfile = open(arguments[2],mode='w')
        except IOError:
            print('There was an error opening the output file!')
            exit(-1);
    else:
        outfile = sys.stdout
    arguments[2] = outfile
    return arguments


# evaluate a single operand, it's either a reference or a number (for now)
def myeval(op, line):
    if op.find("#") >= 0:
        index = op[1:]
        index = int(index)
        fields = line.split(',')
        # we assume fields denoted starting at 1, arrays start at 0
        return int(fields[index - 1])
    else:
        return int(op)


# evaluates the condition on the line of input to produce a truth value.
# only simple conditions for now.

def apply(condition, line):
    if (condition[0] == '>'):
        return (myeval(condition[1], line) > myeval(condition[2], line))
    elif (condition[0] == '<='):
        return (myeval(condition[1], line) <= myeval(condition[2], line))
    elif (condition[0] == '>='):
        return (myeval(condition[1], line) >= myeval(condition[2], line))
    elif (condition[0] == '=='):
        return (myeval(condition[1], line) == myeval(condition[2], line))
    elif (condition[0] == '!='):
        return (myeval(condition[1], line) != myeval(condition[2], line))
    else:
        print("wrong or unallowed operator!")
        exit(-1)


"""
this is the part that actually scans through the input and produces the output. First the header is copied if it exists. Then the input is checked line by line and copied if appropriate.
"""


def myselect(arguments):
    condition = arguments[0]
    myinput = arguments[1]
    myinput.seek(0)
    myoutput = arguments[2]
    if arguments[3]:  # this is the header switch
        # copy first line directly from input to output
        myoutput.write(myinput.readline())
    for line in myinput:
        if run1_query_tree(condition, line):
            myoutput.write(line)


# main program starts here
def main():

    #extracting all the arguments
    arguments = user_interface()

    #setting input and output
    arguments = set_input_output(arguments)

    #column offset error handling
    column_offset_validation(arguments)

    #parsing the condition
    try:
        arguments[0] = parsecondition(arguments[0])

        if arguments[0] == None:
            print('something broken in the condition or the parser')
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)



    #print(arguments)

    myselect(arguments)

    arguments[1].close()
    arguments[2].close()
    #querytree = ParseCondition.parsecondition(arguments[0])
    #arguments[0] = parse_condition(arguments[0])
    #print(querytree)


main()

"""
TO DO:
-error checking on condition.
-recursive condition parsing.
-error checking on column offset.
-handling comparisons on strings (how to denote in command line)
-header: allowing column denoted by name.
-additional parameter list for projection.
"""



