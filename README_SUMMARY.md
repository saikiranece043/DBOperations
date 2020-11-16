# Performing Summary Operation on data

#### Examples to run the program

`pypy summary.py -h -c ‘#14’ -f input.csv`
`cat input.csv | pypy summary.py -c '#14, #discount ' -h`

#### Args to the program
   * position of an attribute (-c) Optional
   * Input File Path (-f)
   * Header Flag -h 
   * Line Separator -s (default value ',')

#### Positional Attributes 
   * The argument -c is an optional attribute indicating the column offset
   * In the absence of this argument summary statistics are performed on every attribute
   * If an argument is provided summary statistics are calculated only for the interested attributes


#### Input 
   * The input arg indicates the program should apply the condition on the contents of the file
   * Input data to the program can also be passed from the standard input

#### Header Flag
   * If the flag -h is found in the command the program would assume the input first line is header
   * In the absence the program would assume there is no header information in the input

#### Separator
   * In the absence of -s the program would assume the input data delimiter is ','
   * User can overwrite this by sending an arg -s with their desired delimiter


### Tasks performed by the program 

   * if a column is of type numeric minimum, maximum, median, mode and standard deviation are calculated
   * if a column is of type string, number of distinct values and a summarized histogram is computed
   * Summarized histogram is made of 5 most common values their frequencies, 5 least common values and their frequencies 
   * If a column has less than 10 distinct values complete histogram is computed
   * Number of missing values in the data is computed
 