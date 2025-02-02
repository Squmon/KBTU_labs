#6
def reverse_sentence(s:str):
    return ''.join(map(lambda x: x+' ', reversed(s.split(" "))))
input("print_sentence")

