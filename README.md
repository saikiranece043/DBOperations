#Performing Select Operations on Input Data files

### Sample command from user

`python3 Select.py -c '#1 > 2 and ( #2 >= 5 and #2 = "test" )' -i foo.csv -h -o bar.csv` 

#### Args to the program
   * Condition (-c)
   * inputfile (-i)
   * ouputfile (-o)
   * headerflag -h
   * line separator -s
   * projection ?? 

#### Inputs Validation and Error Handling
   * Validate each input provided by the user
        + Error checking on condition
        + Error checking on column offset
   * Return an appropriate error to the user

#### Parse Condition
   * Simple condition parsing
   * Complex condition parsing
       + Recursive Condition Parsing
   
#### Set Input and Output Arguments
   * Setting the Input File
   * Setting the Output File
 
#### Evaluation of Conditions
   * Evaluate logical operations on each line of input
   * Evaluate Relational operations on each line of input

#### Tidying the Input from user for evaluation
   * Converting data to appropriate type

#### Performing Select Operation
   * Writing the final results 

### Error Handling
  * Tokens handling is performed within 
  * column offset error handling 
       + set the input and output args 