def down(N):
  i = N
  while i >= 0:
    yield i
    i -= 1

print(*down(10))