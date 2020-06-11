# %% TUPLE
'''
10.2 Write a program to read through the mbox-short.txt and figure out the distribution by hour of the
day for each of the messages. You can pull the hour out from the 'From ' line by finding the time and
then splitting the string a second time using a colon.

From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008

Once you have accumulated the counts for each hour,
print out the counts,
sorted by hour as shown below.

04 3
05 2
07 8
10 4
.
.
.

'''

handle = open("coursera/P4E/mbox-short.txt")
dic = dict()
for line in handle:
    if not line.startswith("From"):
        time = line[15:]
print(time)

key = sorted(dic)





# %% top contributing email DICTIONARY


# name = input("Enter file:")
# if len(name) < 1 : name = "mbox-short.txt"

handle = open("coursera/P4E/mbox-short.txt")

lst = list()
for line in handle:
    line = line.strip()
    if line.startswith("From:"):
        words = line.split()
        email = words[1]
        lst.append(email)

dct = dict()

for email in lst:
    dct[email] = dct.get(email,0) +1

bigcount = None
email_address = None
for key,value in dct.items():
    if bigcount is None or value > bigcount:
        bigcount = value
        email_address = key

print (email_address, bigcount)