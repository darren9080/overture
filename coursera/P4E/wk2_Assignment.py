import re

handle1 = open("coursera/P4E/regex_sum_42.txt")
handle2= open("coursera/P4E/regex_sum_737654.txt")



## Finding Numbers in a Haystack ##
#### answer ####

handle1 = open("coursera/P4E/regex_sum_737654.txt")
numbers = 0
for line in handle1:
    line = line.rstrip()
    numbers = numbers + sum(map(lambda x: int(x), re.findall('([0-9]+)', line)))
print(numbers)


## Exploring the HyperText Transport Protocol ##
#### answer ####

handle1 = open("coursera/P4E/regex_sum_42.txt")
numbers = re.findall('[0-9]+',handle1)
new_list = []

print(sum(new_list))

handle1
for line in handle1:
    line = line.rstrip()
    print(line)