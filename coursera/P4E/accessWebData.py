# regular expression - pt1
import re

handle = open("coursera/P4E/mbox-short.txt")

#find function
for line in handle:
    line = line.rstrip()
    if line.find('From:') >=0:
        print(line)

# regex
handle = open("coursera/P4E/mbox-short.txt")
for line in handle:
    line = line.rstrip()
    if re.search('From:',line):
        print(line)
#startswith
handle = open("coursera/P4E/mbox-short.txt")
for line in handle:
    line = line.rstrip()
    if line.startswith("From:"):
        print(line)
# regex
handle = open("coursera/P4E/mbox-short.txt")
for line in handle:
    line = line.rstrip()
    if re.search('^From:',line):
        print(line)

# regular expression - pt1

x = 'My 2 favorite numbers are 19 and 42'
y = re.findall('[0-9]+',x)

y= re.findall('[aeiou]+',x)

# assignment 11

import re
handle = open("coursera/P4E/sample.txt")
for line in handle:
    line = line.rstrip()
    find_int = re.findall('[0-9]+',line)

find_int



re.findall('[aeiou]+',line)


txt = 'what is 12, 123,6412,1624'

re.findall('[0-9]+',txt)

int_list = list(map(int,re.findall('[0-9]+',txt)))
