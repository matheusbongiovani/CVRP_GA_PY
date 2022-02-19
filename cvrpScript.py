import sys
import time
import random
import matplotlib.pyplot as plt
import numpy as np


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

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x


start = time.time()
# cada meta-heurística possui um conjunto de parâmetros cujos
# valores devem ser fornecidos pela entrada
if len(sys.argv) != 2:
    print('----------------------ERROR----------------------')
    print('Sintaxe: python3 "program.py" "instância.vrp" ')
    sys.exit('-------------------------------------------------')
else:
    arg1 = sys.argv[1]

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

# [0[3,1,2]00[6,4,5]00[7,8,9]0]:   fitness_rout([3,1,2])
def fitness_route(route):
    cost = 0
    i = 0

    cost += matrix_distancias[0][route[0].getId()]  #1º nó da rota
    for _ in range(len(route)-1):
        cost += matrix_distancias[route[i].getId()][route[i+1].getId()]
        i += 1
    cost += matrix_distancias[0][route[i].getId()] #último nó da rota
    return cost


# [0[3,1,2]00[6,4,5]00[7,8,9]0]:   fitness_solution([[3,1,2],[6,4,5],[7,8,9]])
def fitness_solution(solution):
    cost = 0
    for route in solution:
        cost += fitness_route(route)
    return cost

###################################### ----
def create_solution(genes_entrada):
    genes = genes_entrada.copy()
    depot = genes.pop(0)

    def k_total_demand(k_set):
        weight = 0
        for gene in k_set:
            weight += gene.getZ()
        return weight

    def possible_solution(genes):
        randomized = random.sample(genes, len(genes))
        lista_de_rotas = [[] for i in range(k_rotas)]

# modelo da solução: [[3,1,2],[6,4,5],[7,8,9]]
        rota_atual = 0
        for gene in randomized:
            if rota_atual == k_rotas:
                rota_atual = 0
            lista_de_rotas[rota_atual].append(gene)
            rota_atual += 1
        
        return lista_de_rotas

    return possible_solution(genes)



def check_population_total_demand(solution):
    total_demand = 0
    for route in solution:
        for gene in route:
            total_demand += float(gene.getZ())
    return total_demand



# sol1 = create_solution(array_of_genes)
# print(check_population_total_demand(sol1))

rota1 = [array_of_genes[1], array_of_genes[10],array_of_genes[5]]


print('demanda total:',population_total_demand(array_of_genes))

# print(fitness_route(rota1))
# print(array_of_genes[0].distance(array_of_genes[1]) +
#       array_of_genes[1].distance(array_of_genes[10]) +
#       array_of_genes[10].distance(array_of_genes[5]) +
#       array_of_genes[5].distance(array_of_genes[0]))


print(f'Número de cidades a serem atendidas: {n_genes}')
print(f'Número de Veículos (número de rotas): {k_rotas}')
print(f'Capacidade máxima do veículo: {k_cap_max}')


possible_solucion = create_solution(array_of_genes)



print_solution(possible_solucion)


# cromoRota = [array_of_genes[0], array_of_genes[5], array_of_genes[10], array_of_genes[11], array_of_genes[0]]




# # # # plt.xkcd()  # deixar visual de quadrinho
# # # # ----------- plot section---------------
# plt.grid(False)
# plt.scatter(x_values(array_of_genes), y_values(
#     array_of_genes), s=20, c='blue')
# plt.scatter(array_of_genes[0].x, array_of_genes[0].y, s=30, c='red')
# def plot_solution(solution):
#     for rota in solution:
#         plt.plot(x_values(rota),y_values(rota))
# plot_solution(possible_solucion)

# plt.show()
# # # ----------------------------------------


# end = time.time()
# print("Tempo de execução:", end-start)
# plt.show()
