import argparse, sys, re
import copy
from prettytable import PrettyTable


def user_interface():
	resultlist = []
	parser = argparse.ArgumentParser(conflict_handler="resolve")
	parser.add_argument("-a", "--attributes", help="group by attributes")
	parser.add_argument("-f", "--function", help="aggregate functions")
	parser.add_argument("-i", "--input", help="input file")
	parser.add_argument("-o", "--output", help="output file")
	parser.add_argument("-h", "--header", default=False, action="store_true", help="whether input file has header")
	parser.add_argument("-s", "--split", default=',', help="line separator")
	args = parser.parse_args()
	resultlist.append(args.attributes)
	resultlist.append(args.input)
	resultlist.append(args.output)
	resultlist.append(args.header)
	resultlist.append(args.split)
	resultlist.append(args.function)
	return resultlist


def column_offset_validation(arguments):
	"""
    This function is to validate the column offset and return user friendly errors
    It also returns the line against which it performs the column reference validation
    :param : arguments - args provided by the user to the program
    :return: returns the first line of the input stream (file or stdin)
    """

	aggattrlist = []

	for func in arguments[5].split(','):
		aggattrlist.append(re.search(r'\((.*?)\)', func).group(1))

	groupingattributes = arguments[0].split(',')

	inputfile = arguments[1]
	header = inputfile.readline()
	splitter = arguments[4]
	attributesCount = len(header.split(splitter))
	# operands = arguments[0].split(',')
	operands = aggattrlist
	hasheader = arguments[3]

	if hasheader:
		for operand in operands:

			# if you are here the column offset can be a integer or string
			if operand[1:].isdecimal():
				data_error_handler(operand, attributesCount, arguments, type="aggregation")
			else:
				# This block of code is executed for float or string
				if operand[1:] not in header:
					print(f'aggregate column reference {operand} entered is incorrect')
					free_resources(arguments)
					sys.exit(-1)

		for attr in groupingattributes:
			if attr.isdecimal():
				data_error_handler("#" + str(attr), attributesCount, arguments, type="grouping")
			else:
				# This block of code is executed for float or string
				if attr not in header:
					print(f'grouping column reference {operand} entered is incorrect')
					free_resources(arguments)
					sys.exit(-1)


	else:
		# no header so setting the file pointer back to first line
		# if inputtype != None: (while going back is an option in files not for stdin)
		#    inputfile.seek(0)
		for operand in operands:
			if operand[1:].isdecimal():
				data_error_handler(operand, attributesCount, arguments, type="aggregation")
			else:
				print(f'grouping column reference {operand} cannot be a string, perhaps you forgot to pass "-h" arg')
				free_resources(arguments)
				sys.exit(-1)

		# print(groupingattributes)
		for attr in groupingattributes:
			if attr.isdecimal():
				data_error_handler("#" + str(attr), attributesCount, arguments, type="grouping")
			else:
				# This block of code is executed for float or string
				print(f'aggregate column reference {operand} cannot be a string, perhaps you forgot to pass "-h" arg')
				free_resources(arguments)
				sys.exit(-1)

	return header


def data_error_handler(data, attributesCount, arguments, type):
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
		print(f'The column offset {data}  in {type} should be an integer')
		free_resources(arguments)
		sys.exit(-1)
	# the column offset should be between 0...(attributesCount - 1)
	if int(data[1:]) not in range(1, attributesCount + 1):
		print(f'The column offset {data} in {type} should be in the range (1, {attributesCount - 1}) ')
		free_resources(arguments)
		sys.exit(-1)


def free_resources(arguments):
	"""
    Function to close the input and output file or stdin/out references
    :param arguments:
    :return: void
    """
	arguments[1].close()
	arguments[2].close()


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
			outfile = open(arguments[2], mode='w')
		except IOError:
			print('There was an error opening the output file!')
			exit(-1);
	else:
		outfile = sys.stdout
	arguments[2] = outfile
	return arguments


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
		# return get_type(cvalue)
		return type_conversion(cvalue)
	# if a column is referred by its name
	else:
		cvalue = fields[arguments[-1][index]]
		return type_conversion(cvalue)


def type_conversion(val):
	'''
	Function to convert the input string to int or float
	:param val:
	:return: int or float
	'''
	if val.isdecimal():
		return int(val)
	else:
		try:
			return float(val)
		except:
			print("Aggregations on string data type cannot be performed")
			sys.exit(-1)


def aggregate_func(aggfunc, line, args, attr, init):
	'''
	Function to perform simple aggregations conditionally
	:param aggfunc:
	:param line:
	:param args:
	:param attr:
	:param init:
	:return: aggregation result
	'''
	if aggfunc == 'sum':
		val = myeval(attr, line, args)
		return val + init
	elif aggfunc == 'count':
		return init + 1
	elif aggfunc == 'avg':
		val = myeval(attr, line, args)
		init[0] = init[0] + 1
		init[1] = val + init[1]
		init[2] = init[1] / init[0]
		return init
	elif aggfunc == 'min':
		initialmin = init[1]
		if initialmin:
			val = myeval(attr, line, args)
			return (val, False)
		else:
			val = myeval(attr, line, args)
			return (val, False) if val < init[0] else (init[0], False)

	elif aggfunc == 'max':
		initialmax = init[1]
		if initialmax:
			val = myeval(attr, line, args)
			return (val, False)
		else:
			val = myeval(attr, line, args)
			return (val, False) if val > init[0] else (init[0], False)
	else:
		print("Unsupported aggregate Operation")
		free_resources(args)
		sys.exit(-1)


def group_by_hash(args, firstline):
	'''
	Performing aggregations in groups using a dictionary
	:param args:
	:param firstline:
	:return: results
	'''
	attributes, input, output, hasheader, split, aggfunc = args
	aggfunclists = aggfunc.split(',')
	attrlist = attributes.split(',')

	aggattrlist = []
	aggfunclist = []

	for func in aggfunclists:
		aggattrlist.append(re.search(r'\((.*?)\)', func).group(1))
		aggfunclist.append(func.split('(')[0])

	# a dct to hold the aggregation values
	results = {}

	if hasheader:
		# This path is taken when the user passes header argument
		# cols holds the header name and its index in a dict for later use
		cols = {}
		for idx, col in enumerate(firstline.split(split)):
			cols[col.strip('\n')] = idx

		args.append(cols)

		for idx, attr in enumerate(attrlist):
			try:
				int(attr)
			except:
				attrlist[idx] = cols[attr] + 1

		# aggregating the rest of the lines in file or stdin reading line by line
		for line in input:
			datalist = line.split(split)
			groupingstring = "|".join([datalist[int(attr) - 1] for attr in attrlist])

			if groupingstring in results:
				# you have to update the results in the previous iteration
				for index in range(0, len(aggattrlist)):
					results[groupingstring][index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index],
					                                                results[groupingstring][index])

			else:
				# you would have to reset the init value and then update it
				results[groupingstring] = reset_init(aggfunclist, args)
				for index in range(0, len(aggattrlist)):
					results[groupingstring][index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index],
					                                                results[groupingstring][index])

	else:

		# performing multiple aggregations on first line to ensure the results are accurate
		datalist = firstline.split(split)
		groupingstring = "|".join([datalist[int(attr) - 1] for attr in attrlist])
		results[groupingstring] = reset_init(aggfunclist, args)

		for index in range(0, len(aggattrlist)):
			results[groupingstring][index] = aggregate_func(aggfunclist[index], firstline, args, aggattrlist[index],
			                                                results[groupingstring][index])

		# performing multiple aggregations per line and stored the results in dict
		for line in input:
			datalist = line.split(split)
			groupingstring = "|".join([datalist[int(attr) - 1] for attr in attrlist])

			if groupingstring in results:
				# you have to update the results in the previous iteration
				for index in range(0, len(aggattrlist)):
					results[groupingstring][index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index],
					                                                results[groupingstring][index])
			else:
				# you would have to reset the init value and then update it
				results[groupingstring] = reset_init(aggfunclist, args)
				for index in range(0, len(aggattrlist)):
					results[groupingstring][index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index],
					                                                results[groupingstring][index])

	return results


def reset_init(aggfunclist, args):
	'''
	Resetting the init
	:param aggfunclist:
	:param args:
	:return:
	'''
	init = []
	for aggfunc in aggfunclist:
		if aggfunc == 'sum' or aggfunc == 'count':
			init.append(0)
		elif aggfunc == 'min' or aggfunc == 'max':
			init.append((0, True))
		elif aggfunc == 'avg':
			init.append([0, 0, 0])
		else:
			print("Unsupported Aggregate function")
			free_resources(args)
			sys.exit(-1)
	return copy.deepcopy(init)


def pretty_print(results, args):
	'''
	This function is  to print the final results to stdoutput
	:param results:
	:param args:
	:return: void
	'''
	attributes, input, output, hasheader, split, aggfunc = args
	aggfunclists = aggfunc.split(',')

	aggattrlist = []
	aggfunclist = []

	for func in aggfunclists:
		aggattrlist.append(re.search(r'\((.*?)\)', func).group(1))
		aggfunclist.append(func.split('(')[0])

	aggfunclists.insert(0, 'GroupBy')
	t = PrettyTable(aggfunclists)
	for k, v in results.items():
		drow = []
		drow.append(k)
		for idx, value in enumerate(v):
			if aggfunclist[idx] == 'sum' or aggfunclist[idx] == 'count':
				drow.append(value)
			elif aggfunclist[idx] == 'min' or aggfunclist[idx] == 'max':
				drow.append(value[0])
			elif aggfunclist[idx] == 'avg':
				drow.append(value[2])
		t.add_row(drow)
	print(t)


def main():
	args = user_interface()
	args = set_input_output(args)
	print(args)
	firstline = column_offset_validation(args)
	results = group_by_hash(args, firstline)
	pretty_print(results, args)


main()
