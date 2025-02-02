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

