#Author: Greg Donaldson
#Purpose: Created for the purpose of pulling data from the .dat files for Freedom in the Galaxy. 
#Primarily for use by the backend team. This will need to updated as we pull more information
#from different .dat files.

import io
import sys

#This function is used for files that use commas to space out values present.

def commaOnly(file):
    dataList = []
    f = open(file, 'r')
    for line in f:
        if line[0] == '#':
            continue
        elif line[-1] == '\n':
            temp = line[:(len(line)-1)].split(',') 
            dataList.append(temp)
        else:
            temp = line.split(',')
            dataList.append(temp)
    
    return dataList

#This function is used with files that space out values with a comma followed by a space.
    
def commaWithSpace(file):
    dataList = []
    f = open(file, 'r')
    for line in f:
        tempList = []
        if line[0] == '#':
            continue
        else:
            temp = line.split(', ')
            for split in temp:
                if len(split) > 2 and split[-2] == ',':
                    tempList.append(split[:-2])
                else:
                    tempList.append(split)
            dataList.append(tempList)
    
    return dataList
        
#This function is for files that use only commas to seperate values, but end a line with a semi-colon.        
        
def commasAndSemiColon(file):
    dataList = []
    f = open(file, 'r')
    for line in f:
        tempList = []
        if line[0] == '#':
            continue
        else:
            temp = line.split(',')
            for split in temp:
                if len(split) > 2 and split[-2] == ';':
                    tempList.append(split[:-2])
                else:
                    tempList.append(split)
            dataList.append(tempList)
    
    return dataList
    
#This function is solely for pulling races out of races.dat.
    
def raceSnag(file):
    dataList = []
    f = open(file, 'r')
    for line in f:
            tempList = []
            if line[0] == '#':
                continue
            else:
                temp = line.split(',')
                for split in temp:
                    if len(split) > 2 and split[-2] == ',':
                        tempList.append(split[:-2])
                    elif len(split) > 2 and split[-2] == '_':
                        environ = split[-1]
                        tempList.append(split)
                        tempList.append(environ)
                    elif split == '\n':
                        continue
                    else:
                        tempList.append(split)
                dataList.append(tempList)

    return dataList