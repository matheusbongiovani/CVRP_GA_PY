import sys
import time
import random
import Genetic
import matplotlib.pyplot as plt
import numpy as np


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

i = 0
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
                node = Genetic.Gene(float(split_id_XY[1]), float(
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
                array_of_genes[i].z = splitZ[1]
                i += 1
###---- fim da leitura da entrada ----

depot_node = array_of_genes[0]
n_genes = i  # len(array_of_genes)
# obter valor K, que representa o número de veículos dado pela entrada
k_rotas = header_array[0].split('-k')
k_rotas = int(k_rotas[1])
k_cap_max = float(header_array[5])


def print_genes_list(genes_list):
    for gene in genes_list:
        print(gene.__str__())


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


def create_n_cromossomo(genes_entrada, k_num, k_cap, size_pop):
    genes = genes_entrada
    depot = genes.pop(0)
    population = []

    def capacidade_ocupada_rota(rota):
        cap_ocupada = 0
        for gene in rota:
            cap_ocupada += gene.getZ()
        return cap_ocupada

    def create_solution(rand_genes):
        solution = []
        rota_k = []            
        randomized = random.sample(rand_genes, len(rand_genes))
        for gene in randomized:
            if capacidade_ocupada_rota(rota_k) > float(k_cap):
                solution.append(rota_k)
                rota_k.clear()
            else:
                rota_k.append(gene)   
        return solution

    for elem in range(size_pop):

        possible_solution = create_solution(genes)
        if(len(possible_solution) <= k_num):
            population.append(possible_solution)
        else:
            while(len(possible_solution) > k_num):
                possible_solution = create_solution(genes)
                if(len(possible_solution) < k_num):
                    population.append(possible_solution)
                    break
    return population

population = create_n_cromossomo(array_of_genes, k_rotas, k_cap_max, 100)

print(population[0][3])

print(f'Número de cidades a serem atendidas: {n_genes}')
print(f'Número de Veículos (número de rotas): {k_rotas}')
print(f'Capacidade máxima do veículo: {k_cap_max}')


# # plt.xkcd()  # deixar visual de quadrinho
# # ----------- plot section---------------
plt.grid(False)
plt.scatter(x_values(array_of_genes), y_values(
    array_of_genes), s=20, c='blue')
plt.scatter(array_of_genes[0].x, array_of_genes[0].y, s=30, c='red')
plt.show()
# # ----------------------------------------


# end = time.time()
# print("Tempo de execução:", end-start)
# plt.show()
