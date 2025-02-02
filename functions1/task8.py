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
