n = int(input())
even_generator = (i for i in range(0, n) if i % 2 == 0)
print(*even_generator, sep = ", ")
