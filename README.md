#Performing Select Operations on Input Data files

### Sample commands from user

`python3 select.py -c '#1 > 2 and ( #2 >= 5 and #2 = "test" )' -i foo.csv -h -o bar.csv`
`python3 select.py -c '#1 > 2 and ( #2 >= 5 and #2 = "test" )' -i foo.csv -h -o bar.csv -p '#1,#2'` 

#### Args to the program
   * Condition (-c)
   * inputfile (-i)
   * ouputfile (-o)
   * headerflag -h
   * line separator -s (default value ',')
   * projection -p

#### Condition arg passed to the user
   * Condition is parsed by the ply lexer and parser
   * Extracts the tokens from the condition and a query tree is generated
   * The query tree is applied on each line of the input recursively

#### Input to the program
   * The input arg indicates the program should apply the condition on the contents of the file
   * Input data to the program can also be passed from the standard input

#### Output
   * Program would write the output to the file provided by the user in command as arg -o '{filename}'
   * The output would be written to the standard output if the user doesn't pass -o argument to the program
 
#### Header Flag
   * If the flag -h is found in the command the program would assume the input first line is header
   * In the absence the program would assume there is no header information in the input 

#### seperator
   * In the absence of -s the program would assume the input data delimiter is ','
   * User can overwrite this by sending an arg -s with their desired delimiter 

#### Projection
   * In the absence of projection the program wouldn't reduce the data written to output
   * In the presence of projection arg the program would write only the desired data to output stream

