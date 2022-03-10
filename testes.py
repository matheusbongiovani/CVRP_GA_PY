import random

pop = [0, 1, 2, 3, 4, 3, 9, 5, 6, 7, 8, 9]

newpop = []

x = random.sample(pop, 4)   
y = random.sample(pop, 4)

# print(line, end='')
# list_of_lists = [[] for i in range(5)]
# list comprehension
# a = [i*2 for i in range(0,10)]    
# a = [ 2*x for x in [i for i in range(0,10)]]
# b = {str(x): x for x in range(0,10)}


l0 = [1]
l1 = [1, 2, 3]
l2 = [5, 3, 2, 9, 4, 5, 6, 7]

#a porra da função NÃO ALTERA os dados do parametro, apenas lê...
# def rmv(l2):
#     l2 = l1
#     return l2

# print(l2)
# print(rmv(l2))
# print(l2)

asdf = [0, 52, 53, 54, 18, 20, 41, 0, 6, 10, 26, 46, 63, 62, 16, 0, 50, 47, 61, 37, 30, 7, 55, 0, 32, 58, 40, 8, 65, 33, 42, 0, 27, 5, 14, 9, 12, 49, 0, 51, 34, 43, 22, 35, 56, 13, 1, 0, 28, 25, 48, 59, 44, 64, 0, 17, 23, 45, 31, 19, 38, 57, 11, 0, 24, 2, 36, 21, 39, 29, 3, 60, 4, 15, 0]
aaa = asdf.sort()
print(asdf)



ssss = sum([83.0, 90.0, 97.0, 100.0, 89.0, 85.0, 84.0, 91.0, 11.0])
print(ssss)

# print(l2[-2:])
