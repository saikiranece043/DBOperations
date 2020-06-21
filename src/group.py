import argparse, sys, re, subprocess
import copy

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


def sort_input(args):
	attributes, input, output, hasheader, split, aggfunc = args
	cmd = [ "sort", "-k", attributes , "-t", split ]
	proc = subprocess.Popen(cmd,stdin=input, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
	o, e = proc.communicate()
	#print('Output: ' + o.decode('ascii'))

	with open("sortedfile","w") as f:
		f.write(o.decode())



def group_by(args):

	attributes, input, output, hasheader, split, aggfunc = args
	input = open("sortedfile")
	aggfunclists = aggfunc.split(',')
	attrlist = attributes.split(',')

	aggattrlist = []
	aggfunclist = []

	for func in aggfunclists:
		aggattrlist.append(re.search(r'\((.*?)\)', func).group(1))
		aggfunclist.append(func.split('(')[0])



	# an array to hold the aggregation values
	init = []
	init = reset_init(aggfunclist,args,init)

	# initiating variables
	firstIteration = True
	currentgroupstring = ""
	previousgroupstring = ""

	# reading line by line and performing aggregations
	for line in input:
		datalist = line.split(split)
		currentgroupstring = "".join([datalist[int(attr)-1] for attr in attrlist])

		# executed only once for the first time
		if firstIteration:
			firstIteration = False
			for index in range(0, len(aggattrlist)):
				init[index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index], init[index])
			previousgroupstring =  currentgroupstring

		else:
			## that means same group so keep incrementing
			if currentgroupstring == previousgroupstring:
				for index in range(0, len(aggattrlist)):
					init[index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index], init[index])
			## you are here means new group flush the init values to stdout or file, reset the init value
			else:
				output.write(previousgroupstring + " ")
				output.write(" ".join([str(x) for x in init]))
				output.write('\n')
				init = []
				init = reset_init(aggfunclist, args, init)
				for index in range(0, len(aggattrlist)):
					init[index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index], init[index])
				previousgroupstring = currentgroupstring

	output.write(previousgroupstring + " ")
	output.write(" ".join([str(x) for x in init]))
	output.write('\n')





def group_by_hash(args):

	attributes, input, output, hasheader, split, aggfunc = args
	aggfunclists = aggfunc.split(',')
	attrlist = attributes.split(',')

	aggattrlist = []
	aggfunclist = []

	for func in aggfunclists:
		aggattrlist.append(re.search(r'\((.*?)\)', func).group(1))
		aggfunclist.append(func.split('(')[0])



	# an array to hold the aggregation values

	results = {}


	firstiter = True
	# reading line by line and performing aggregations
	for line in input:
		datalist = line.split(split)
		groupingstring = "".join([datalist[int(attr)-1] for attr in attrlist])

		if groupingstring in results:
				# you have to update the results in the previous iteration

				for index in range(0, len(aggattrlist)):
					results[groupingstring][index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index], results[groupingstring][index])

		else:
				# you would have to reset the init value and then update it
				print("new group ",groupingstring)

				results[groupingstring] = reset_init(aggfunclist,args)

				for index in range(0, len(aggattrlist)):
					results[groupingstring][index] = aggregate_func(aggfunclist[index], line, args, aggattrlist[index], results[groupingstring][index])



	print(results)




def reset_init(aggfunclist,args,init=[]):

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




def main():
	args = user_interface()
	args = set_input_output(args)
	print(args)
	sort_input(args)
	group_by(args)
	#group_by_hash(args)





main()