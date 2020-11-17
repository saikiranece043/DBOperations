[![Build Status](https://dev.azure.com/s0pott05/glennissolutions/_apis/build/status/saikiranece043.DBOperations?branchName=master)](https://dev.azure.com/s0pott05/glennissolutions/_build/latest?definitionId=4&branchName=master)

# Performing Select Operations on User Input

#### Examples to run the program

`pypy3 select.py -c '#1 > 2 and ( #2 >= 5 and #2 == "test" )' -i foo.csv -h -o bar.csv`

`pypy3 select.py -c '#1 > 2 and ( #2 >= 5 and #2 == "test" )' -i foo.csv -h -o bar.csv -p '#1,#2' -s '|'`

#### Args to the program
   * Condition (-c)
   * Input File Path (-i)
   * Output File Path (-o)
   * Header Flag -h 
   * Line Separator -s (default value ',')
   * Projection -p

#### Condition 
   * Condition is parsed by the ply lexer and parser
   * Extracts the tokens from the condition and a query tree is generated
   * The query tree is applied on each line of the input recursively

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

#### Projection
   * In the absence of projection the program wouldn't reduce the data written to output
   * In the presence of projection arg the program would write only the desired data to output stream

#### Positive Scenario Work Flow Chart

<img width="757" alt="Screen Shot 2020-06-07 at 10 27 12 PM" src="https://user-images.githubusercontent.com/12020642/83987591-c6e8c000-a90e-11ea-96cd-25131a5c45a3.png">
```
