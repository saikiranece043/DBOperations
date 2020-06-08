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
    parser.add_argument("-p", "--projection", help="columns to project")
    args = parser.parse_args()
    resultlist.append(args.condition)
    resultlist.append(args.input)
    resultlist.append(args.output)
    resultlist.append(args.header)
    resultlist.append(args.split)
    resultlist.append(args.projection)
    return resultlist



def free_resources(arguments):
    """
    Function to close the input and output file or stdin/out references
    :param arguments:
    :return: void
    """
    arguments[1].close()
    arguments[2].close()



def column_offset_validation(arguments):
    """
    This function is to validate the column offset and return user friendly errors
    It also returns the line against which it performs the column reference validation
    :param : arguments - args provided by the user to the program
    :return: returns the first line of the input stream (file or stdin)
    """
    inputfile = arguments[1]
    header = inputfile.readline()
    splitter = arguments[4]
    attributesCount = len(header.split(splitter))
    operands = arguments[0].split()
    hasheader = arguments[3]

    if hasheader:
        for operand in operands:
            if operand.startswith('#'):
                #if you are here the column offset can be a integer or string
                if operand[1:].isdecimal():
                    data_error_handler(operand,attributesCount,arguments)
                else:
                    # This block of code is executed for float or string
                    if operand[1:] not in header:
                        print(f'column reference {operand} entered is incorrect')
                        free_resources(arguments)
                        sys.exit(-1)

    else:
        #no header so setting the file pointer back to first line
        #if inputtype != None: (while going back is an option in files not for stdin)
        #    inputfile.seek(0)
        for operand in operands:
            if operand.startswith('#'):
                if operand[1:].isdecimal():
                    data_error_handler(operand,attributesCount,arguments)
                else:
                    print(f'column reference {operand} cannot be a string, perhaps you forgot to pass "-h" arg')
                    free_resources(arguments)
                    sys.exit(-1)
    return header



def data_error_handler(data,attributesCount,arguments):
    """
    Function performs validation of the input data
    Checks if the data is string or integer
    If the data is integer it further checks if it's contained within a range
    :param data: data to validate for errors
    :param attributesCount: number of columns in the input
    :param arguments: args provided by the user to the program
    :return: void
    """
    # if you are here that means the column offset should always be an integer

    if not data[1:].isdecimal():
        print(f'The column offset {data} should be an integer')
        free_resources(arguments)
        sys.exit(-1)
    # the column offset should be between 0...(attributesCount - 1)
    if int(data[1:]) not in range(0,attributesCount):
        print(f'The column offset {data} should be in the range (0, {attributesCount - 1 }) ')
        free_resources(arguments)
        sys.exit(-1)



"""
arguments[1] is the name of an input file or None. To get a file descriptor, the file is open; if None, standard input is used. This way, the rest of the program works with a file descriptor regardless of where the data comes from.
Similarly for output. This allows working with pipes.
"""


def set_input_output(arguments):
    '''
    function to set the input(file or stdin)and output(file or stdout) references
    :param arguments: args provided by the user to the program
    :return: arguments with output and input references updated
    '''
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


"""
this is the part that actually scans through the input and produces the output. First the header is copied if it exists. Then the input is checked line by line and copied if appropriate.
"""


def myselect(arguments,firstline):
    """
    Function to perform selection on each line of the input
    :param arguments: args provided by the user to the program
    :param firstline: firstline of the input
    :return: void
    """
    condition = arguments[0]
    myinput = arguments[1]
    myoutput = arguments[2]
    projection = arguments[5]
    hasheader = arguments[3]
    splitter = arguments[4]
    totalcols = len(firstline.split(splitter))

    if hasheader:  # this is the header switch

        # column names and the index numbers are stored as dictionary for quick access in the loop
        # This is handled early for performance gains
        cols = {}
        for idx,name in enumerate(firstline.split(splitter)):
            cols[name.strip('\n')] = idx
        arguments.append(cols)

        # copy first line directly from input to output
        myoutput.write(firstline)

        #translating the user column references of projection to numbers
        # this is handled early for performance gain
        colstoproject = []
        for colref in projection.split(','):
            if colref[1:].isdecimal():
                if colref[1:] not in range(0, totalcols):
                    print("The column referenced in projection by number is invalid")
                    sys.exit(-1)
                colstoproject.append(int(colref[1:])-1)
            else:
                if colref[1:] not in firstline.split(splitter):
                    print("The column referenced in projection by name is invalid")
                    sys.exit(-1)
                colstoproject.append(int(cols[colref[1:]]))

        # if projection is required a different path to be taken
        # This is to avoid conditional check within the loop
        if projection:
            for line in myinput:
                if run1_query_tree(condition, line, arguments):
                    line = projection_cols(line,colstoproject)
                    myoutput.write(line)

        # projection is not required here
        else:
            for line in myinput:
                if run1_query_tree(condition, line, arguments):
                    myoutput.write(line)
    else:

        # if projection is required a different path to be taken
        # This is to avoid conditional check within the loop
        if projection:


            # translating the user column references of projection to numbers
            colstoproject =[]

            for colref in projection.split(','):
                if colref[1:].isdecimal():
                    colrefi = int(colref[1:])
                    if colrefi not in range(0,totalcols):
                        print("The column referenced in projection by number is not invalid")
                        sys.exit(-1)
                    colstoproject.append(colrefi - 1)
                else:
                    print("The column referenced in projection by number is a string so invalid")
                    sys.exit(-1)


            # selection performed on the first line
            if run1_query_tree(condition, firstline, arguments):
                tooutput = projection_cols(firstline,colstoproject)
                myoutput.write(tooutput)

            #selection performed on each of the rest of the lines
            for line in myinput:
                if run1_query_tree(condition, line, arguments):
                    tooutput = projection_cols(line,colstoproject)
                    myoutput.write(tooutput)
        else:
            if run1_query_tree(condition, firstline, arguments):
                myoutput.write(firstline)
            for line in myinput:
                if run1_query_tree(condition, line, arguments):
                    myoutput.write(line)


def projection_cols(line,projectedcols):
    """
    The function takes a row and returns a modified row with required columns data
    :param line: line in the input
    :param projectedcols: cols to project to output
    :return: user interested columns data separated by a separator
    """
    rowdata = line.split('|')
    result ="|".join([rowdata[columnNumber] for columnNumber in projectedcols])
    return result + '\n'


# main program starts here
def main():

    #extracting all the arguments
    arguments = user_interface()

    #setting input and output
    arguments = set_input_output(arguments)

    #column offset error handling (for header true and false)
    #grabbing the firstline to ensure we evaluate all lines
    firstline = column_offset_validation(arguments)

    #print(arguments)ls
    #parsing the condition

    try:
        arguments[0] = parsecondition(arguments[0])
        if arguments[0] == None:
            print('something broken in the condition or the parser')
            sys.exit(-1)
    except Exception as e:
        free_resources(arguments)
        print(e)
        sys.exit(-1)

    myselect(arguments,firstline)
    free_resources(arguments)

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



