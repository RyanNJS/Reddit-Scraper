from collections import Counter
import csv
def word(fname):
    with open(fname, errors='ignore') as f:
        return Counter(f.read().split())

print(word("PostsText.txt"))

my_dict = word("PostsText.txt")
with open('test.csv', 'w') as f:
    for key in my_dict.keys():
        if my_dict[key] > 1:
            # print("%s,%s\n"%(key,my_dict[key]))
            f.write("%s,%s\n"%(key,my_dict[key]))
