#Performing Select Operations on User Input

### Sample commands from user

`python3 select.py -c '#1 > 2 and ( #2 >= 5 and #2 = "test" )' -i foo.csv -h -o bar.csv`

`python3 select.py -c '#1 > 2 and ( #2 >= 5 and #2 = "test" )' -i foo.csv -h -o bar.csv -p '#1,#2'`

#### Args to the program
   * Condition (-c)
   * input file (-i)
   * output file (-o)
   * header flag -h
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

#### separator
   * In the absence of -s the program would assume the input data delimiter is ','
   * User can overwrite this by sending an arg -s with their desired delimiter

#### Projection
   * In the absence of projection the program wouldn't reduce the data written to output
   * In the presence of projection arg the program would write only the desired data to output stream

### Flow of the program

```flow
st=>start: Start
e=>end: End
op1=>operation: User Interface
op2=>operation: Setting Input Args
op3=>operation: Column Offset Validation
op4=>operation: Parsing Condition
op5=>operation: Select
op6=>operation: Execute QTree
op7=>operation: projection


st->op1(down)->op1
op1->op2(right)->op2
op2->op3(down)->op3
op3->op3(right)->op4
op4->op5(down)->op5
op5->op5(right)->op6
op6->op6(right)->op7
op7->op7(right)->e
```
