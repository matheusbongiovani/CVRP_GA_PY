from os import dup
import sys
import time
import random
import matplotlib.pyplot as plt
import numpy as np


# adicionar rota a qual a cidade está inserida? self.rota = rota
class Gene(object):

    def __init__(self, x=0, y=0, z=0, id=0):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    # fazer matriz de distancias para economizar contas repitidas
    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return ((dx**2) + (dy**2))**0.5

    def getX(self):
        return float(self.x)

    def getY(self):
        return float(self.y)

    def getZ(self):
        return float(self.z)

    def getId(self):
        return int(self.id)

    def __str__(self):
        return 'id:' + str(self.getId()) + ' (' + str(self.getX()) + ',' + str(
            self.getY()) + ')' + ' demand:' + str(self.getZ())
    
    def __repr__(self):
        return 'id:' + str(self.getId())

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return ((self.id) < (other.id))


start = time.time()
# cada meta-heurística possui um conjunto de parâmetros cujos
# valores devem ser fornecidos pela entrada
if len(sys.argv) != 4:
    print('----------------------ERROR----------------------')
    print('Sintaxe: python3 "program.py" "instância.vrp" "população" "prob mutação(0.5)" ')
    sys.exit('-------------------------------------------------')
else:
    arg1 = sys.argv[1]
    arg_size = sys.argv[2]
    arg_mutate = sys.argv[3]
    

header_array = []
array_of_genes = []

index_entrada = 0
with open(arg1, mode='r', encoding='utf-8') as file:
    # file.read()
    # print(file.read())

    num_linha = 0
    gene_coord_bool = False
    demand_section_bool = False

    for linha in file:

        # print(line, end='')
        # trecho para armazenar informações do cabeçalho
        if num_linha < 6:
            num_linha += 1
            splited = linha.split()
            header_array.append(splited[2])

        # trecho para pular linhas da entrada que não será utilizado
        if num_linha >= 6 and num_linha < 9:
            num_linha += 1
            if num_linha > 8:
                gene_coord_bool = True

        # trecho para armazenar as posições no vetor array_of_genes
        if gene_coord_bool:
            if linha.find('DEMAND_SECTION') != -1:
                gene_coord_bool = False
                demand_section_bool = True

            else:
                split_id_XY = linha.split()
                node = Gene(float(split_id_XY[1]), float(
                    split_id_XY[2]), id=(int(split_id_XY[0])-1))
                array_of_genes.append(node)

        # trecho para inserir a demanda de cada nó no vetor array_of_genes
        if demand_section_bool:
            if linha.find('DEMAND_SECTION') != -1:
                continue
            if linha.find('DEPOT_SECTION') != -1:
                demand_section_bool = False
            else:
                splitZ = linha.split()
                array_of_genes[index_entrada].z = splitZ[1]
                index_entrada += 1
# ---- fim da leitura da entrada ----

n_genes = index_entrada  # len(array_of_genes)

# obter valor K, que representa o número de veículos dado pela entrada
k_rotas = header_array[0].split('-k')
k_rotas = int(k_rotas[1])
k_cap_max = float(header_array[5])


def print_genes_list(genes_list):
    for gene in genes_list:
        print(gene.__str__())

def print_solution(solution):
    print('[', end='')
    for rota in solution:
        print('0 ', end='')
        for gene in rota:
            print(gene.getId(),end=' ')
        # print('', end='')
    print('0]', end='')


def x_values(genes_list):
    list_x = []
    for gene in genes_list:
        list_x.append(gene.getX())
    return list_x


def y_values(genes_list):
    list_y = []
    for gene in genes_list:
        list_y.append(gene.getY())
    return list_y



def population_total_demand(genes_list):
    total_demand = 0
    for gene in genes_list:
        total_demand += float(gene.getZ())
    return total_demand


def func_matrix_distancias(genes):
    matrix_ij = []
    size = len(genes)
    for i in range(size):
        a = []
        for j in range(size):
            a.append(genes[i].distance(genes[j]))
        matrix_ij.append(a)
    return matrix_ij

matrix_distancias = func_matrix_distancias(array_of_genes)

#fitness_solution([9, 3, 0, 2, 4, 0, 5, 6, 0, 8, 7, 1])
#os depots no meio do vetor já estão inseridos, precisamos adicionar o 1º e o último
def fitness(solution):
    cost = 0
    i = 0

    cost += matrix_distancias[0][solution[0].getId()]  #1º nó da 1ª rota
    for _ in range(len(solution)-1):
        cost += matrix_distancias[solution[i].getId()][solution[i+1].getId()]
        i += 1
    cost += matrix_distancias[0][solution[i].getId()] #último nó da última rota
    return cost


# tornar a solução factível, fazendo com que atenda as restrições do problema.
# solução inicial sempre vai ser factivel... Aplicar ela após mut/cross
def turn_feasible(cromo):
    genes_seq = array_of_genes.copy()
    genes_seq.pop(0)
    sorted = cromo.copy()
    sorted.sort()
    # cities_seq = [i for i in range(1,len(cromo)+1)]
    missing = []
    duplicates = []

    # percorer a solução ordenada para verificar se faltam cidades (havendo duplicatas)
    for gene in genes_seq:
        if gene not in sorted:
            missing.append(gene)

    index = 0
    while index < len(cromo):
        if index < len(cromo)-1:
            if sorted[index].getId() == sorted[index+1].getId():
                duplicates.append(sorted[index])
        index += 1
    
    
    # substituir as duplicadas pelas cidades que estão faltando
    if duplicates:
        dup_aux = duplicates.copy()
        dpc_i = 0
        i = 0
        while i < len(cromo):
            if dpc_i < len(missing) and cromo[i] in dup_aux:
                dup_aux.remove(cromo[i])
                cromo[i] = missing[dpc_i]
                dpc_i += 1
                i += 1
            else:
                i += 1
#   cabo = 0

def route_capacity(cromo):
    total = 0.0
    i = 0
    while i < len(cromo):
        total += cromo[i].getZ()
        if total >= k_cap_max:
            cromo.insert(i, array_of_genes[0])
            total = 0
        i += 1
    # # remoção de depots consecutivos:
    # i = 0
    # while i < len(cromo)-1:
    #     if cromo[i] == 00 and cromo[i+1] == 0:
    #         del cromo[i]
    #     i += 1


def create_initial_population(genes_entrada, pop_size):
    population = []
    genes = genes_entrada.copy()
    depot = genes.pop(0)  # dado a entrada, retiramos o depot

    for i in range(int(pop_size)):
        randomized = random.sample(genes, len(genes))
        population.append(randomized)

    # modelo da solução: [3,1,2,6,4,5,7,8,9]
    return population


# modelo da entrada: [3,1,2,6,4,5,7,8,9]
def create_new_population(pop):
    new_pop = []
    # mutação de inverter trecho do vetor
    def mutation(cromo):
        
        index1 = random.randrange(0,len(cromo))
        index2 = random.randrange(index1,len(cromo))
        
        mid = cromo[index1:index2]
        mid.reverse()
        
        result = cromo[0:index1] + mid + cromo[index2:]
        
        return result       

    def tournament_select_two(old_pop):
        def best_fit_parents():
            selecteds = []
            num_selects = int(len(old_pop)/10)
            candidates = random.sample(old_pop, num_selects)
            best = 999999999  # very large number to always have a better fitness
            for cromo in candidates:
                fitness_value = fitness(cromo)
                if fitness_value < best:
                    selecteds.append(cromo)
                    best = fitness_value
            best_cromo = selecteds.pop()
            return best_cromo
        
        parent1 = best_fit_parents()
        parent2 = best_fit_parents()
        
        return [parent1, parent2]
    
    def crossover(parents):
        # filhos serão construídos através de cortes nos vetores dos pais
        cut1, cut2 = random.randint(1, n_genes-1), random.randint(1, n_genes-1)
        cut1, cut2 = min(cut1, cut2), max(cut1, cut2)

        child1 = parents[0][:cut1] + parents[1][cut1:cut2] + parents[0][cut2:]
        child2 = parents[1][:cut1] + parents[0][cut1:cut2] + parents[1][cut2:]
        new_pop.append(child1)
        new_pop.append(child2)

    # Para termos a população constante, iteramos o tamanho da população divido por 2
    # já que em cada iteração são gerado 2 membros da nova geração
    aaaa = int(len(pop)/2)
    for i in range(int(len(pop)/2)):
        selecteds = tournament_select_two(pop)
        crossover(selecteds)
    
    fitness_score = []
    for solution in new_pop:
        if random.random() < float(arg_mutate):
            mutation(solution)
        turn_feasible(solution)
        route_capacity(solution)
        fitness_score.append(fitness(solution))

    pop = new_pop

def inicializar():
    population = create_initial_population(array_of_genes,arg_size)

    create_new_population(population)



inicializar()


def k_total_demand(k_set):
    weight = 0
    for gene in k_set:
        weight += gene.getZ()
    return weight


def check_population_total_demand(solution):
    total_demand = 0
    for route in solution:
        for gene in route:
            total_demand += float(gene.getZ())
    return total_demand


# print_genes_list(array_of_genes)

rota1 = [array_of_genes[1], array_of_genes[10],array_of_genes[5]]


print('demanda total:',population_total_demand(array_of_genes))

# print(array_of_genes[0].distance(array_of_genes[1]) +
#       array_of_genes[1].distance(array_of_genes[10]) +
#       array_of_genes[10].distance(array_of_genes[5]) +
#       array_of_genes[5].distance(array_of_genes[0]))


print(f'Número de cidades a serem atendidas: {n_genes}')
print(f'Número de Veículos (número de rotas): {k_rotas}')
print(f'Capacidade máxima do veículo: {k_cap_max}')


# cromoRota = [array_of_genes[0], array_of_genes[5], array_of_genes[10], array_of_genes[11], array_of_genes[0]]




# # # # plt.xkcd()  # deixar visual de quadrinho
# # # ----------- plot section---------------
plt.grid(False)
plt.scatter(x_values(array_of_genes), y_values(
    array_of_genes), s=20, c='blue')
plt.scatter(array_of_genes[0].x, array_of_genes[0].y, s=30, c='red')
def plot_solution(solution):
    for rota in solution:
        plt.plot(x_values(rota),y_values(rota))

plt.show()
# # ----------------------------------------


# end = time.time()
# print("Tempo de execução:", end-start)
# plt.show()
