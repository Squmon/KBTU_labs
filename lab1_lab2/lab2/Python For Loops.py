# example 1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

# example 2
for x in "banana":
  print(x)

# example 3
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

# example 4
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

# example 5
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

# example 6
for x in range(6):
  print(x)

# example 7
for x in range(2, 6):
  print(x)

# example 8
for x in range(2, 30, 3):
  print(x)

# example 9
for x in range(6):
  print(x)
else:
  print("Finally finished!")

# example 10
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

# example 11
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

# example 12
for x in [0, 1, 2]:
  pass