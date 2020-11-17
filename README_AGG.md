[![Build Status](https://dev.azure.com/s0pott05/glennissolutions/_apis/build/status/saikiranece043.DBOperations?branchName=master)](https://dev.azure.com/s0pott05/glennissolutions/_build/latest?definitionId=4&branchName=master)
# Performing Simple Aggregations On Attributes

#### Examples to run the program

`pypy3 agg.py -a '#14' -f "max" -s '|' -i foo.csv`

`pypy3 agg.py -a '#14,#discount' -f "max,min" -s '|' -i foo.csv -h -o bar.csv`

#### Conditions of the program
   * The number of attributes and aggregation functions in the input should be same
   * Simple aggregate functions are supported and are to referred by their key names

#### Args to the program
   * Attributes on which aggregations are to be performed (-a)
   * Input File Path (-i)
   * Output File Path (-o)
   * Header Flag -h 
   * Line Separator -s (default value ',')
   * Aggregations to apply on the attributes -f
   
#### Supports Simple Aggregations 
   * sum
   * count
   * avg
   * min
   * max

#### Attributes to apply aggregations on
   * Attributes to apply aggregations are extracted from the input
   * They are validated against the data in the stdin or the input file
   * Aggregation results are written to stdout or output file

#### Input 
   * The input arg indicates the program should apply the condition on the contents of the file
   * Input data to the program can also be passed from the standard input

#### Output
   * Program would write the output to the file provided by the user in command as arg -o '{filename}'
   * The output would be written to the standard output if the user doesn't s -o argument to the program

#### Header Flag
   * If the flag -h is found in the command the program would assume the input first line is header
   * In the absence the program would assume there is no header information in the input

#### Separator
   * In the absence of -s the program would assume the input data delimiter is ','
   * User can overwrite this by sending an arg -s with their desired delimiter

#### Functions
   * These are the simple aggregations to be performed on the grouped data
   * User can pass list of aggregations to be applied for attributes
