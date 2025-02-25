





import random
seed = 3
random.seed(seed)

list1=['a', 'b', 'c', 'd']
list2=[1,2,3,4]

print(len(list2))
print(random.choice(list1))

random.seed(seed+1)
seed+=1
print(random.choice(list2))


1 3 5
2 4 6
