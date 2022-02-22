from random import randrange

chromo = [5, 1, 3, 2, 4]

# print(min(chromo))
print(int(3.1))

def inversion_mutation(chromosome_aux):
    chromosome = chromosome_aux
    
    index1 = randrange(0,len(chromosome))
    index2 = randrange(index1,len(chromosome))
    
    chromosome_mid = chromosome[index1:index2]
    chromosome_mid.reverse()
    
    chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]
    
    return chromosome_result


inverted = inversion_mutation(chromo)

chromosome_mid = inverted[2:5]
chromosome_mid.reverse()
print(chromosome_mid)

# for i in range(30):
#     inverted = inversion_mutation(chromo)
#     print(inverted)
# randrange(5, 5) retorna: empty range for randrange() (5, 5, 0)