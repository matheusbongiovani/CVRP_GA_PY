import random

pop = [0, 1, 2, 3, 4, 3, 9, 5, 6, 7, 8, 9]

newpop = []

x = random.sample(pop, 4)   
y = random.sample(pop, 4)

cutIdx1 = random.randint(1, min(len(x), len(y)) - 1)
cutIdx2 = random.randint(1, min(len(x), len(y)) - 1)
cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)
# Doing crossover and generating two children
child1 = x[:cutIdx1] + y[cutIdx1:cutIdx2] + x[cutIdx2:]
child2 = y[:cutIdx1] + x[cutIdx1:cutIdx2] + y[cutIdx2:]
newpop += [child1, child2]

# print(line, end='')
# list_of_lists = [[] for i in range(5)]
# list comprehension
# a = [i*2 for i in range(0,10)]    
# a = [ 2*x for x in [i for i in range(0,10)]]
# b = {str(x): x for x in range(0,10)}



l1 = [1, 2, 3]
l2 = [5, 3, 2, 9, 4, 5, 6, 7]

print(l2[-2:])

