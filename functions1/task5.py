#5
from itertools import permutations 

perm = permutations(input("give me string"))
print("Here your permutations:") 
for p in perm:
    print(p)

