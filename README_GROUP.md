# Performing simple Aggregations on groups

#### Examples to run the program

`pypy3 group.py -a '#14' -f "max(#1)" -s '|' -i ../resources/test.csv`

`pypy3 group.py -a '#14,#discount' -f "max(#1),min(#quantity)" -s '|' -i '../resources/test.csv' -h -o '../resources/out'`


#### Args to the program
   * Group attributes (-a)
   * Input File Path (-i)
   * Output File Path (-o)
   * Header Flag -h 
   * Line Separator -s (default value ',')
   * Aggregations to apply on the groups -f
   
### Supports Simple Aggregations 
   * sum
   * count
   * avg
   * min
   * max

#### Grouping Attributes 
   * Grouping attributes are extracted from the input
   * They are validated against the data in the stdin or the input file
   * Data is grouped and stored as dictionary key

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
   * User can pass list of aggregations to be applied for a grouping attribute
