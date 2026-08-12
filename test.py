from collections import Counter

def majorityElement(nums):
    num_counter = Counter(nums)
    return max(num_counter, key=num_counter.get)


print(majorityElement([2,2,1,1,1,2,2]))

