## NAPA Invoicing Efficiency Script
## Written by: Troy Paul
## The problem faced was that Napa's transaction records were very difficult for human eyes to read
## This script alleviates that by formatting it all pretty
## Basic algorithm is as follows:   open file
##                                  convert to pandas dataframe 
##                                  adjust column names, reorder, delete unneccessary info, general formatting
##                                  convert to csv
## Inputs: .txt file
## Outputs: .csv file (will be named the same as original txt)
## Dependencies: Pandas
import pandas as pd 
import sys, os, getopt, argparse

## This block parses the input. We have one parameter labelled 'inputfile' 
## All passed arguments are loaded into args our sole paramter is accessed by args.inputfile
parser = argparse.ArgumentParser()
parser.add_argument('inputfile', help= "The File to be Processed")
args = parser.parse_args()

## Opens the input file if no such file exists, this will throw an error
## The temp file test.txt exists so that we don't override critical data
## Notice we opened the input with 'r' or read variable and the temp with 'w' or write
temp_path = "test.txt"
input_path = args.inputfile
source= open(input_path, 'r') 
temp = open(temp_path, 'w')

## There were certain lines that could be deleted. They deliniated the input into different invoices
## The seperating lines were exactly 25 characters.
## lines stores the whole txt file with extra metadata about each line
## Since we are done with the source material we can close it
## Loops through each line comparing the string length, when not equal to 25 the line is added else its skipped
## Have to close temp because we need to open it in read form later
lines = source.readlines()
source.close()
for line in lines:
    if (len(line)!=25):
        print(line, file = temp)
temp.close()

## Columns_names are in order that they were read from initial txt
## Useful_columns are listed in the new desired order though this constructor ignores order
## Open temp back in read mode
## df is a 2d array or DataFrame
## pd.read_csv(FILE, SEPERATOR TOKEN, SPECIFY IF FIRST ROW HAS HEADER DATA, LABEL COLUMNS, ONLY LOAD THE USEFUL COLUMNS, SKIP BLANK LINES)
## Close and delete temp
columns_names = ["Shop ID", "Message 2", "NAPA Invoice", "Date", "Quantity", "UoM", "Total","Detail Type", "Line Code", "Part Number", "Part Description", "Section", "Message 1"]
useful_columns= [1,4,5,8,9,13,14,10,18,17,3,11,12]
temp = open(temp_path, "r")
df = pd.read_csv(temp, sep = '|', header = None, names = columns_names, usecols= useful_columns,skip_blank_lines=True)
temp.close()
try:
    os.remove(temp_path)
except:
    e = sys.exc_info()[0]
    print("Error: %s" % e)

## Further formatting:
## Drops all rows that have column[detail type] == Tax
## After Tax lines dropped remove columns detail type and line code
## Finally reorder the columns
index = df[df['Detail Type'] == 'TAX'].index
df.drop(index, inplace = True)
df.drop(['Detail Type','Line Code', 'Section'], axis = 1, inplace=True)
try:
    df= df[['Shop ID', 'NAPA Invoice', 'Date', 'Quantity', 'UoM', 'Part Number', 'Part Description', 'Total', 'Message 1', 'Message 2']]
except:
    e = sys.exc_info()[0]
    print("Error: %s" % e)

sum = df.sum(axis = 0, numeric_only = True)
date = df['Date']

## Changes the name of the inputfile to csv 
## The way this was done, you can put a relative path in as a paramater and it will place the new file in the same relative spot
name = args.inputfile.replace('.txt', '.csv')
df.to_csv(name)

print(round(sum['Total'], 2), date[0])