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
        return str(self.getId())

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
    arg_mutate = float(sys.argv[3])
    

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
                array_of_genes[index_entrada].z = float(splitZ[1])
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
        total_demand += (gene.getZ())
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
    cost += matrix_distancias[solution[i].getId()][0] #último nó da última rota
    return cost


# tornar a solução factível, fazendo com que atenda as restrições do problema.
# solução inicial sempre vai ser factivel... Aplicar ela após mut/cross
genes_seq_entrada = array_of_genes.copy()
genes_seq_entrada.pop(0)  # remover depot 
#[0, 1, 4, 3, 0, 2, 2, 6, 0]   NÃO TÁ FUNFANDO DIREITO....
def turn_feasible(cromo_entrada):
    global genes_seq_entrada
    cromo = cromo_entrada.copy()
    sorted = cromo.copy()
    sorted.sort()
    # cities_seq = [i for i in range(1,len(cromo)+1)]

    duplicates = True
    while duplicates:
        duplicates = False
        for i1 in range(len(cromo)):
            for i2 in range(i1):
                if cromo[i1] == cromo[i2]:
                    noDuplicates = True
                    for id in genes_seq_entrada:
                        if id not in cromo:
                            cromo[i1] = id
                            noDuplicates = False
                            break
                    if noDuplicates:
                        del cromo[i1]
                    duplicates = True
                if duplicates: break
            if duplicates: break


    #separar cidades em rotas # mudar jeito de como distribuir a demanda...
    def distribuir_demand(cromo_aux):
        crmo = cromo_aux.copy()
        total = 0.0
        i = 0
        while i < len(crmo):
            total += crmo[i].getZ()
            if total >= k_cap_max:
                crmo.insert(i, array_of_genes[0])
                total = 0
            i += 1
        return crmo
        
    cromo = distribuir_demand(cromo)
    comolen = len(cromo)
    # remoção de possíveis depots consecutivos:
    i = 0
    while i < len(cromo)-1:
        if cromo[i].getId() == 0 and cromo[i+1].getId() == 0:
            del cromo[i]
        i += 1

    caboporra = 0
    
    return cromo



def create_initial_population(genes_entrada, pop_size):
    population = []
    genes = genes_entrada.copy()
    depot = genes.pop(0)  # dado a entrada, retiramos o depot

    for i in range(int(pop_size)):
        randomized = random.sample(genes, len(genes))
        randomized = turn_feasible(randomized)
        population.append(randomized)

    fsafsa =0
    # modelo da solução: [3,1,2,6,4,5,7,8,9]
    return population


# modelo da entrada: [3,1,2,6,4,5,7,8,9]
def create_new_population(pop_entrada, mutate_prob):
    pop = pop_entrada.copy()
    new_pop = []

    # mutação de inverter trecho do vetor
    def mutation(cromo, prob_mutate):
        if random.random() < float(prob_mutate):

            index1 = random.randrange(0,len(cromo))
            index2 = random.randrange(index1,len(cromo))
            
            mid = cromo[index1:index2]
            mid.reverse()
            
            result = cromo[0:index1] + mid + cromo[index2:]
            return result     
        else:
            return cromo  

    def tournament_select_two(old_pop):
        def best_fit_parents():
            selecteds = []
            num_selects = int(len(old_pop)/10) # limitar pop mín em torno de 10 elems.
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
    
    def crossover_mutate_and_add_to_new_generation(parents):
        # filhos serão construídos através de cortes nos vetores dos pais
        cut1, cut2 = random.randint(1, n_genes-1), random.randint(1, n_genes-1)
        cut1, cut2 = min(cut1, cut2), max(cut1, cut2)

        child1 = parents[0][:cut1] + parents[1][cut1:cut2] + parents[0][cut2:]
        child2 = parents[1][:cut1] + parents[0][cut1:cut2] + parents[1][cut2:]

        child1 = mutation(child1, mutate_prob)
        child1 = mutation(child1, mutate_prob)

        child1 = turn_feasible(child1)
        child2 = turn_feasible(child2)

        new_pop.append(child1)
        new_pop.append(child2)

    # Para termos a população constante, iteramos o tamanho da população divido por 2
    # já que em cada iteração são gerado 2 membros da nova geração
    aaaa = int(len(pop)/2)
    for i in range(int(len(pop)/2)):
        selecteds = tournament_select_two(pop)
        crossover_mutate_and_add_to_new_generation(selecteds)

    return new_pop


def inicializar():
    population = create_initial_population(array_of_genes,arg_size)

    aaaa = [fitness(i) for i in population]
    mutate_prob = float(arg_mutate)
    index_geracao_atual = 0
    index_iteracoes_sem_melhora = 0
    best_solution_between_gens = population[0] #tem que iniciar com algum valor
    best_solution = None
    best_Fitness = 99999999999
    
    for i in range(1000):
        population = create_new_population(population, mutate_prob)
        index_geracao_atual += 1

        for solution in population:
            fit_value = fitness(solution)
            if fit_value < best_Fitness:
                best_Fitness = fit_value
            best_solution_atual = solution
        
        if best_solution_atual == best_solution:
            index_iteracoes_sem_melhora += 1
            mutate_prob += 0.01
        else:
            best_solution = best_solution_atual
            index_iteracoes_sem_melhora = 0
            mutate_prob = arg_mutate
        
        if fitness(best_solution) <= fitness(best_solution_between_gens):
            best_solution_between_gens = best_solution



    bbbbb = [fitness(i) for i in population]


    print(f'iterações sem melhora:{index_iteracoes_sem_melhora}, prob_mutate:{mutate_prob}')

    oloco = 0
    return best_solution_between_gens


#não tá subs as duplicadas antes de eu aplicar o turn_feasible ali ^ ... turn_feasible tá oredenando!!!!!!!!!! e removendo todos depot
best_reached_solution = inicializar()


def check_population_total_demand(solution):
    total_demand = 0
    for route in solution:
        for gene in route:
            total_demand += (gene.getZ())
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


def route_demand(solution):
    rotas = solution.copy()
    demanda_rotas = []
    demanda = 0.0
    for gene in rotas:
        demanda += gene.getZ()
        if gene.getId()== 0 and demanda != 0:
            demanda_rotas.append(demanda)
            demanda = 0
    demanda_rotas.append(demanda)
    return demanda_rotas

# def return_routes(solution):
#     rotas = solution.copy()
#     for gene in rotas:
#         demanda += gene.getZ()
#         if gene.getId()== 0 and demanda !=:
#             demanda_rotas.append(demanda)
#             demanda = 0
#     demanda_rotas.append(demanda)
#     return demanda_rotas
        
        
print(f'demanda das rotas {route_demand(best_reached_solution)}')
# best_reached_solution.insert(0, array_of_genes[0])
# best_reached_solution.insert(-1, array_of_genes[0])

print(best_reached_solution, fitness(best_reached_solution))


# # # # # plt.xkcd()  # deixar visual de quadrinho
# # # ----------- plot section---------------
plt.grid(False)
plt.scatter(x_values(array_of_genes), y_values(
    array_of_genes), s=20, c='blue')
plt.scatter(array_of_genes[0].x, array_of_genes[0].y, s=30, c='red')
# def plot_solution(solution):
#     for rota in solution:
#         plt.plot(x_values(rota),y_values(rota))

plot_sol = best_reached_solution.copy()
plot_sol.insert(0,array_of_genes[0])
plot_sol.append(array_of_genes[0])

print(f'plot_sol: {plot_sol}')
# list_to_plot = []
# for each in plot_sol:
#     list_to_plot.append(each)
#     if each.getId() == 0:
#         list_to_plot.append(array_of_genes[0])
#         plot_sol.insert(0,array_of_genes[0])
#         plt.plot(x_values(list_to_plot),y_values(list_to_plot))
#         list_to_plot.clear()


plt.plot(x_values(plot_sol),y_values(plot_sol))

plt.show()
# # # ----------------------------------------


# end = time.time()
# print("Tempo de execução:", end-start)
# plt.show()
