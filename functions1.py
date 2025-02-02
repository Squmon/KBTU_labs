#1
converter = lambda grams: 28.3495231 * grams

#2
converter_f = lambda F: (5 / 9) * (F - 32)
print(converter_f(10))

#3

def solve(numheads, numlegs):
    return {
        "rabbits": (r:=((numlegs - 2*numheads)//2)),
        "chickens" : numheads - r,
    }

print(solve(35, 94))
#4

def isprime(number):
    for j in range(2, number):
        if number % j == 0:
            return False
    return True

def filter_prime(l:list[int]):
    return [n for n in l if isprime(n)]

print("Here the primes:", filter_prime(map(int, input("enter the list of numbers").split(" "))))


#5
from itertools import permutations 

perm = permutations(input("give me string"))
print("Here your permutations:") 
for p in perm:
    print(p)

#6
def reverse_sentence(s:str):
    return ''.join(map(lambda x: x+' ', reversed(s.split(" "))))
input("print_sentence")

#7
def has_33(nums):
    filter_33 = [3, 3]
    for i in range(len(nums) - len(filter_33)):
        if nums[i:(i+len(filter_33))] == filter_33:
            return True
    return False

#8 
def spy_game(nums):
    f = [0, 0, 7]
    c = 0
    for j in f:
        for n in nums[c:]:
            if j == n:
                c+=1
                break
        else:
            continue
        return False
    return True

#9
def volume_of_sphere(r):
    return 3.1415*r**3 * 4/3
#10

def unique(l:list):
    q = []
    for e in l:
        if e not in l:
            q.append(e)
    return q

#11

def isPalindrome(s:str):
    return s == reversed(s)

#12

def histogram(a:list[int]):
    for c in a:
        print("*"*c)


#13

from random import randrange

N = randrange(1, 21)
count = 1
name = input("Hello! What is your name?")
print(f"Well, {name}, I am thinking of a number between 1 and 20.")

while (n:= input("Take a guess.")) != N:
    count += 1
    if n < N:
        print("Your guess is too low.")
    else:
        print("Your guess is too high.")

print(f"Good job, KBTU! You guessed my number in {count} guesses!")

#14
from task9 import volume_of_sphere
print(volume_of_sphere(10))