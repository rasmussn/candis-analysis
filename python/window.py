'''
This Python script creates a single file from a set of candis files.
The output file contains subarrays of the input data based on
window ranges: var1 start1 stop1, var2 start2 stop2, ...
'''

import string
import subprocess
import sys
from glob import glob

if len(sys.argv) < 5:
   print("usage: python window.py basename var1 start1 stop1 ...")
   quit()

basename = sys.argv[1]

## find input files to work on
#
files = glob(basename+".[0-9]*")

cmd = ["cdfwindow"]
for i in range(2,len(sys.argv)):
   cmd.append(sys.argv[i])

print(cmd)

## create a subset of each file
#
for file in files:
   print("windowing file: " + file)
   subprocess.check_call(cmd, stdin=open(file), stdout=open(file+".win","w"))

## merge the files together
#
print("merging files:")
cmd = ["cdfcatf"] + glob(basename+".[0-9]*.win")
print(cmd)

subprocess.check_call(cmd, stdout=open(basename+".win", "w"))
