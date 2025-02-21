from math import tan, pi

n = int(input("number of sides: "))
a = int(input("length of each side: "))

S = n*a**2/(4*tan(pi/n))
print("area of polygonn is", S)