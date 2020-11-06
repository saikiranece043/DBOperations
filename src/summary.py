import argparse, sys
import math, operator


def user_interface():
    resultlist = []
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-h", "--header", default=False, action="store_true", help="whether input file has header")
    parser.add_argument("-c", "--position", help="number or list of numbers separated by commas")
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-s", "--split", default='|', help="line separator")
    args = parser.parse_args()
    resultlist.append(args.header)
    resultlist.append(args.input)
    resultlist.append(args.output)
    resultlist.append(args.position)
    resultlist.append(args.split)
    return resultlist



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



def num_stats(newvalue, aggvalue, firstcall=False):
    '''
    '''

    prevmin, prevmax, count, mean, m2, median = aggvalue

    if firstcall:
        maximum = newvalue
        minimum = newvalue
    else:
        minimum = newvalue if newvalue < prevmin else prevmin
        maximum = newvalue if newvalue > prevmax else prevmax

    count += 1
    delta = newvalue - mean
    mean += delta / count
    delta2 = newvalue - mean
    m2 += delta * delta2

    return [minimum, maximum, count, mean, m2, median]


def finalize(existingAggregate):
    (count, mean, M2) = existingAggregate
    if count < 2:
        return float('nan')
    else:
       (mean, variance, sampleVariance) = (mean, M2 / count, M2 / (count - 1))
       return (mean, variance, sampleVariance)




def file_summary(args,firstline):

    header, input, output, pos, splitter = args
    needsecondpass = False

    # if there is header take this route
    if header:
        for file in input:
            line = file.split(splitter)
    else:
        # setting up variables and initiliazing
        stringcols = []
        numericcols = []
        stringsdict = {}
        numericdict = {}
        nullscounter = {}
        stringcolssecondpass = []
        medianlist = {}
        modeslist = {}

        if pos:
            for index, item in enumerate(firstline.split(splitter)):
                index = index + 1
                if index in [int(pos) for pos in pos.split(',')]:
                    a, b = convert_type(item)
                    if b == "string":
                        stringcols.append(index)
                    else:
                        numericcols.append(index)
                for col in numericcols:
                    numericdict[col] = [0, 0, 0, 0, 0, 0]
                    nullscounter[col] = 0
                    medianlist[col] = []
                    modeslist[col] = {}
                for col in stringcols:
                    stringsdict[col] = {}
                    nullscounter[col] = 0
        else:

            for index,item in enumerate(firstline.split(splitter)):
                a,b = convert_type(item)
                if b == "string":
                    stringcols.append(index + 1)
                else:
                    numericcols.append(index + 1)
            for col in numericcols:
                numericdict[col] = [0,0,0,0,0,0]
                nullscounter[col] = 0
                medianlist[col] = []
                modeslist[col] = {}
            for col in stringcols:
                stringsdict[col] = {}
                nullscounter[col] = 0


        for index,item in enumerate(firstline.split(splitter)):
            index = index + 1
            if index in numericcols:
                try:
                    a = float(item)
                    medianlist[index].append(a)


                    numericdict[index] = num_stats(a, numericdict[index], firstcall= True)

                    #keeping a counter on number of times we have seen a value
                    try:
                        modeslist[index][item] = modeslist[index][item] + 1
                    except KeyError:
                        modeslist[index][item] = 1

                except ValueError:
                    if not item.strip():
                        nullscounter[index] += 1

            elif index in stringcols:
                try:
                    if not item.strip():
                        nullscounter[index] += 1
                    else:
                        stringsdict[index][item] = stringsdict[index][item] + 1
                except KeyError:
                    stringsdict[index][item] = 1


        for line in input:
            rowdata = line.split(splitter)
            for index,item in enumerate(rowdata):
                index = index + 1
                if index in numericcols:
                    try:
                        currentitem = float(item)

                        # finding median of medians
                        if len(medianlist[index]) == 5:
                            medianlist[index].sort()
                            numericdict[index][5] = medianlist[index][2]
                            medianlist[index] = []
                        else:
                            medianlist[index].append(currentitem)

                        # keeping a counter on number of times we have seen a value
                        try:
                            modeslist[index][item] = modeslist[index][item] + 1
                        except KeyError:
                            modeslist[index][item] = 1



                        numericdict[index] = num_stats(currentitem, numericdict[index])

                    except ValueError:
                        if not item.strip():
                                nullscounter[index] += 1
                        else:
                            numericcols.remove(index)
                            stringcolssecondpass.append(index)
                            needsecondpass = True

                elif index in stringcols:
                    try:
                        if not item.strip():
                            nullscounter[index] += 1
                        else:
                            stringsdict[index][item] = stringsdict[index][item] + 1
                    except KeyError:
                        stringsdict[index][item] = 1



        if needsecondpass:
            pass


        # clear the median list
        medianlist.clear()

        # print the summary stats of numeric data
        for k,v in numericdict.items():
            mean, variance, samplevariance = finalize(v[2:5])
            sd = math.sqrt(variance)
            freqdict = modeslist[k]
            mode = sorted(freqdict.items(), key= operator.itemgetter(1), reverse= True)[0][0]
            print(f'col {k} min {v[0]} max {v[1]} mean {v[3]} median {v[5]} mode {mode} sd {sd} nulls {nullscounter[k]}')

        # clearing the numeric items in the dictionary
        numericdict.clear()


        # print the summary stats of categorical data
        for k,v in stringsdict.items():

            sorted_data = sorted(v.items(),key= operator.itemgetter(1),reverse=True)
            stringsdict[k] = {}
            distinct = 0
            for tuple_data in sorted_data:
                if tuple_data[1] == 1:
                    distinct += 1

            print(f'column {k} top 5 {sorted_data[:5]}  bottom 5 {sorted_data[-5:]} distinct {distinct} nulls {nullscounter[k]}')

        # clearing string items in the dictionary
        stringsdict.clear()


def convert_type(data:str):
    try:
        return float(data),"number"
    except:
        return data,"string"


def main():
    args = user_interface()
    args = set_input_output(args)
    firstline = args[1].readline()
    file_summary(args,firstline)
    args[1].close()

main()

'''

Objective 

I'm looking to find the summary of all columns (working on a data set with nearly 16 columns)

First step is to identify the data type as each data type needs to be handled differently
- if the method is we are going to read first few rows and decide then we need to remember them
- if we need to read all rows and decide, that would be one pass without doing any other operations

Say the columns are of type numeric 

calc minimum, maximum, mean - can be done out of memory in one pass
mode can be done out of memory, but certain cases the dictionary might be large
standard deviation - can't be done out of memory in one pass 
median - can't be done out of memory unless the input is sorted 
number of missing values - missing values counter 

Say the columns are of type string

distinct values : a dict to count 
summarized histogram - 5 most common values and frequencies and 5 least common values and frequencies (can be calculated in memory)
number of missing values - missing values counter 


find number of distinct values
find top most occurrences
for least 5 occurrences 
'''



