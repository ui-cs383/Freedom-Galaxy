#Author: Greg Donaldson
#Purpose: Created for the purpose of pulling data from the .dat files for Freedom in the Galaxy. 
#Primarily for use by the backend team. This will need to updated as we pull more information
#from different .dat files.

import io
import sys

def planets(file):
    i = 0
    dataList = []
    f = open(file, 'r')
    for line in f:
        if i == 0 :
            i += 1
            continue
        else:
            temp = line[:(len(line)-1)].split(',')
            dataList.append(temp)
        i += 1
    
    return dataList
