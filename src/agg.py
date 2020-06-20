import argparse, sys
from itertools import count,islice

def user_interface():
	resultlist = []
	parser = argparse.ArgumentParser(conflict_handler="resolve")
	parser.add_argument("-a", "--attributes", help="list of attributes")
	parser.add_argument("-f", "--function", help="aggregates")
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
	inputfile = arguments[1]
	header = inputfile.readline()
	splitter = arguments[4]
	attributesCount = len(header.split(splitter))
	operands = arguments[0].split(',')
	hasheader = arguments[3]

	if hasheader:
		for operand in operands:

			# if you are here the column offset can be a integer or string
			if operand[1:].isdecimal():
				data_error_handler(operand, attributesCount, arguments)
			else:
				# This block of code is executed for float or string
				if operand[1:] not in header:
					print(f'column reference {operand} entered is incorrect')
					free_resources(arguments)
					sys.exit(-1)

	else:
		# no header so setting the file pointer back to first line
		# if inputtype != None: (while going back is an option in files not for stdin)
		#    inputfile.seek(0)
		for operand in operands:
			if operand[1:].isdecimal():
				data_error_handler(operand, attributesCount, arguments)
			else:
				print(f'column reference {operand} cannot be a string, perhaps you forgot to pass "-h" arg')
				free_resources(arguments)
				sys.exit(-1)
	return header


def data_error_handler(data, attributesCount, arguments):
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
	if int(data[1:]) not in range(0, attributesCount):
		print(f'The column offset {data} should be in the range (0, {attributesCount - 1}) ')
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
	if val.isdecimal():
		return int(val)
	else:
		try:
			return float(val)
		except:
			print("Aggregations on string data type cannot be performed")
			sys.exit(-1)


def aggregate_func(aggfunc, line, args, attr, init):
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


def lines_count(input, hasheader):
	return sum(1 for line in input) if hasheader else sum(1 for line in input) + 1


def read_blocks(file, size=65536):
	while True:
		data_blocks = file.read(size)
		if not data_blocks:
			break
		yield data_blocks


def group_line(args, firstline):
	# destructuring of the arguments
	attr, input, output, hasheader, split, aggfunc = args
	# print(f' attribute {attr}  aggfun {aggfunc}')
	aggfunclist = args[5].split(',')
	attrlist = args[0].split(',')

	if len(attrlist) != len(aggfunclist):
		print("The number of attributes and aggregate functions should be same")
		free_resources(args)
		sys.exit(-1)

	if len(aggfunclist) == 1 and aggfunclist[0] == 'count':
		return sum(block.count('\n') for block in read_blocks(input))

	## aggregate function value presets
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

	if hasheader:

		cols = {}
		for idx, col in enumerate(firstline.split(split)):
			cols[col.strip('\n')] = idx

		args.append(cols)

		for line in input:
			for index in range(0, len(attrlist)):
				init[index] = aggregate_func(aggfunclist[index], line, args, attrlist[index], init[index])
	else:

		for index in range(0, len(attrlist)):
			init[index] = aggregate_func(aggfunclist[index], firstline, args, attrlist[index], init[index])

		for line in input:
			for index in range(0, len(attrlist)):
				init[index] = aggregate_func(aggfunclist[index], line, args, attrlist[index], init[index])



	return init


def main():
	## extracting the user arguments
	args = user_interface()

	# setting input and output
	args = set_input_output(args)
	firstline = column_offset_validation(args)

	## command to run the aggregation and returns the results
	agg_results = group_line(args, firstline)

	print(agg_results)
	free_resources(args)


main()
