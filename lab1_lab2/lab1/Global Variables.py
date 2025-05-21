# example 1
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()

# example 2
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

# example 3
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)

# example 4
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)