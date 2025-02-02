#4

def isprime(number):
    for j in range(2, number):
        if number % j == 0:
            return False
    return True

def filter_prime(l:list[int]):
    return [n for n in l if isprime(n)]

print("Here the primes:", filter_prime(map(int, input("enter the list of numbers").split(" "))))


