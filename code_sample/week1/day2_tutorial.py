"""
Introduction to python with:
    - navigating a file system from python
    - variable assignment
    - objects and classes
    - indexing and slicing in strings, lists and (numpy) arrays
    - loop: for statement
    - conditionals: if else if statement

get inflammation data from GitHub: https://github.com/kln-courses/tmgu17

"""

###
# preamble, the stuff I need to do before everything else
import os
wd = '/home/kln/Desktop/tutorial_py'
os.chdir(wd)

weight_kg = 55
print weight_kg 

weight_lb = weight_kg * 2.2 
print 'weight in pounds is:', weight_lb

weight_kg = 100
print weight_kg

print weight_lb

import numpy
dir(numpy)# list of functions in numpy
data = numpy.loadtxt(fname='data/inflammation-01.csv', delimiter=',')

print type(data)
print data.dtype
print data.shape
print data

print 'first value is:', data[0,0]

print data[0,0],data[0,1],data[0,2],data[0,3]
print 'is the same as:'
print data[0,0:4]

## slicing a numpy array (or matrix)
print data[0,0:4]# slicing columns
print data[0:4,0]# slicing rows
print data[0:4,0:4]# slicing rows and columns

var = data[0,0:10]# assign slice to variable
print var

# OBJECTS
print 'object', type(var), 'has:'
print ' - attributes', var.dtype# attribute
print ' - methods', var.mean()# method that belong to the object class
print ' - the data in itself is an attribute:', var

numpy.mean(data)
data.mean()
max(data)
data.max()
numpy.max(data)

data_mean, data_max =  numpy.mean(data), numpy.max(data)


## strings
word = 'Darth Vader'
print word
print type(word)

print word[0:5]
print word

title = word[0:5]
print word, 'is a', title

# print chars of string object
print word[0]
print word[1]
print word[2]
print word[3]
print word[4]
# scales badly

## repeat things with loops
# loop over chars in string
for char in word:
    print char

for char in 'Yoda':
    print char

# loop over strings in list    
sw_list = ['Darth Vader', 'Han Solo', 'Yoda']
print sw_list    
for s in sw_list:
    print s
# loops can be embedded
for s in sw_list:
    print '-----'
    for char in s:
        print char
    
# out of index
s = 'Yoda'
print s[0]
print s[4]
# check length with len()
print len(s)
print len(sw_list)    
    
## updating a variable in the loop
letter = 'z' 
for letter in 'abc':
    print letter    
print letter    

# count variable in the loop
s = 'Yoda'
i = 0
for char in s:
    print i
    i = i + 1
print s, 'has', i ,'characters'

#### return to strings
s1 = 'Darth'
s2 = 'Vader'
s3 = s1 + ' ' + s2

print s3

## create string s2 which is reverse char order in string s1
# using string concatenation '+'
s1 = 'Vader'
s2 = ''
for char in s1:
    s2 = char + s2
print s2    


#### making choices
var = 1
if var > 25:
    print 'bigger than 25'
else:
    print 'smaller than or equal to 25'

print 'da' == 'da'    

lang_list = ['lat', 'lat', 'eng', 'eng', 'NA']

if lang_list[0] == 'lat':
    print 'latin'
elif lang_list[0] == 'eng':
    print 'english'
else:
    print 'unknown'

if 'content':
    print 'we have content'

if '':
    print 'we have no content'

if 0:
    print 'hello world'

# applied example: write non-empty strings from list of strings to new list of strings
a_list = ['hello','world','','something']
clean_list = []
for s in a_list:
    if s:
        clean_list.append(s)

print clean_list
