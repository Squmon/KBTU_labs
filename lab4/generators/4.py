def squares(a, b):
  i = a
  while i <= b:
    yield i**2
    i += 1

print(*squares(2, 16))