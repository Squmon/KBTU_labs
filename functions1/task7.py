#7
def has_33(nums):
    filter_33 = [3, 3]
    for i in range(len(nums) - len(filter_33)):
        if nums[i:(i+len(filter_33))] == filter_33:
            return True
    return False

