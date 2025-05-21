# example 1
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)

# example 2
thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)

# example 3
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist)

# example 4
thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse = True)
print(thislist)

# example 5
def myfunc(n):
  return abs(n - 50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)

# example 6
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist)

# example 7
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key = str.lower)
print(thislist)

# example 8
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.reverse()
print(thislist)