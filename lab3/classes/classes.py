class UpperStringOperatinos:
    def __init__(self):
        self.__string = ''

    def getString(self):
        self.__string = input()
    def printString(self):
        print(self.__string.upper())


class Shape:
    def area(self):
        return 0
    

class Square(Shape):
    def __init__(self, length):
        super().__init__()
        self.length = length

    def area(self):
        return self.length**2
    

class Rectange(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
        super().__init__()

    def area(self):
        return self.length*self.width
    
class Point:
    def __init__(self, position:list[int]):
        self.position = position

    def move(self, to:list[int]):
        self.position = to

    def show(self):
        print("position:",self.position)

class Account:
    def __init__(self, owner:str, balance:int = 0):
        self.owner:str = owner
        self.__balance:int = balance

    def deposit(self, amount:int):
        self.__balance += amount
    
    def withdraw(self, amount:int):
        if self.__balance >= amount:
            self.__balance -= amount
            return amount
        q = self.__balance
        self.__balance = 0
        return q

class programm_that_use_filter_to_get_filter_prime_numbers_realization_in_class:
    def run(self, l:list):
        return [*filter(lambda x:all(not x%i == 0 for i in range(2, x)) and x != 1, l)]
    
print(programm_that_use_filter_to_get_filter_prime_numbers_realization_in_class().run([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 111211]))
