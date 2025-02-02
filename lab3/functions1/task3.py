#3

def solve(numheads, numlegs):
    return {
        "rabbits": (r:=((numlegs - 2*numheads)//2)),
        "chickens" : numheads - r,
    }

print(solve(35, 94))
