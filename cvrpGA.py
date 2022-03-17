import sys
import time
import random
import matplotlib.pyplot as plt

#Classe Gene, que representa as cidades da instância.
class Gene(object):
    def __init__(self, x=0, y=0, demand=0, id=0):
        self.x = x
        self.y = y
        self.demand = demand
        self.id = id
    # Posteriormente anexado à matriz de distancias reduzindo contas repitidas
    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return ((dx**2) + (dy**2))**0.5

    def __str__(self):
        return 'id:' + str(self.id) + ' (' + str(self.x) + ',' + str(
            self.y) + ')' + ' demand:' + str(self.demand)
    
    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return ((self.id) < (other.id))


start_time = time.time()
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
    num_linha = 0
    gene_coord_bool = False
    demand_section_bool = False

    for linha in file:
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
                array_of_genes[index_entrada].demand = float(splitZ[1])
                index_entrada += 1
# ---- fim da leitura da entrada ----

n_genes = len(array_of_genes)
# k_rotas: nº de veículos(rotas) passado pela entrada
k_rotas = header_array[0].split('-k')
k_rotas = int(k_rotas[1])
k_cap_max = float(header_array[5])

initial_mutate_prob = 0.05  # mutação padrão de 5%
num_elem_pop = (n_genes-1)*2  # nºcidades-depot * 2
time_to_execute = 300   # Tempo de execução do algoritmo em segundos


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


def removeZeros(cromo):
    for each in cromo:
        if each.id == 0:
            cromo.remove(each)

def distribuirZerosNaSol(cromo):
    i = 0
    total = 0
    while i < len(cromo):
        total += cromo[i].demand  #Se demanda de i exceder, o Depot é inserido imediatamente antes
        if total > k_cap_max:
            cromo.insert(i, array_of_genes[0])
            total = 0
        i += 1

def removerZerosDolado(cromo):
    i = 0
    while i<(len(cromo)-1):
        if cromo[i].id == 0 and cromo[i+1].id==0:
            del cromo[i]
            continue
        i += 1

#modelo fitness_solution([9, 3, 0, 2, 4, 0, 5, 6, 0, 8, 7, 1]) == Cromossomo
#os depots no meio do vetor já estão inseridos, precisamos adicionar o 1º e o último
#[6, 5, 4, 3, 1, 2, 9, 8]
def fitness(solution):

    removerZerosDolado(solution)
    cost = 0
    i = 0

    cost += matrix_distancias[0][solution[0].id]  #1º nó da 1ª rota
    for _ in range(len(solution)-1):
        cost += matrix_distancias[solution[i].id][solution[i+1].id]
        i += 1
    cost += matrix_distancias[solution[i].id][0] #último nó da última rota

#  Checar nº de rotas, e aplicar penalidade caso exceda capacidade máxima
    i = 0
    num_of_depots = 1

    while i < len(solution):
        if solution[i].id == 0:
            num_of_depots += 1
        i += 1

    if num_of_depots != k_rotas:
        i = 0
        weight = 0
        penalty = 0
        while i < len(solution):
            weight += solution[i].demand
            if solution[i].demand == 0:
                if weight > k_cap_max:
                    # penalty*50 performed better
                    penalty += (weight - k_cap_max)*50
                    cost += penalty
                    weight = 0
            i += 1
    return cost

genes_seq_entrada = array_of_genes.copy()
genes_seq_entrada.pop(0)  # array com todas as cidades exceto o depot
def turn_feasible(cromo_entrada):
    cromo = cromo_entrada.copy()

    removeZeros(cromo)

    adjust = True
    while adjust:
        adjust = False
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
                    adjust = True
                if adjust: break
            if adjust: break

    # separar cidades em rotas quando o veículo não conseguir carregar demanda da próx cidade
    total = 0.0
    i = 0   

    distribuirZerosNaSol(cromo)
    # removerZerosDolado(cromo)  
    
    return cromo


def create_initial_population(genes_entrada, pop_size):
    population = []
    genes = genes_entrada.copy()
    depot = genes.pop(0)  # dado a entrada, retiramos o depot

    for i in range(int(pop_size)):
        randomized = random.sample(genes, len(genes))
        randomized = turn_feasible(randomized)
        population.append(randomized)

    # modelo da solução: [3,1,2,6,4,5,7,8,9]
    return population


# Mutação: inverte trecho do vetor da solução
def mutation(cromo, prob_mutate=0.05):
    if random.random() < float(prob_mutate):

        index1 = random.randrange(0,len(cromo))
        index2 = random.randrange(index1,len(cromo))
        
        mid = cromo[index1:index2]
        mid.reverse()
        
        result = cromo[0:index1] + mid + cromo[index2:]
        return result
    else:
        return cromo

# Método de Seleção: Torneio
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


def crossover(parents):
    # filhos serão construídos através de cortes nos vetores dos pais

    pai1 = parents[0]
    pai2 = parents[1]
    removeZeros(pai1)
    removeZeros(pai2)

    leen = min(len(pai1),len(pai2))
    cut1, cut2 = random.randrange(leen), random.randrange(leen)

    cut1, cut2 = min(cut1, cut2), max(cut1, cut2)

    child1 = pai1[:cut1] + pai2[cut1:cut2] + pai1[cut2:]
    child2 = pai2[:cut1] + pai1[cut1:cut2] + pai2[cut2:]
    
    distribuirZerosNaSol(pai1)
    distribuirZerosNaSol(pai2)

    distribuirZerosNaSol(child1)
    distribuirZerosNaSol(child2)

    return child1, child2

def create_new_population(pop_entrada, prob_mutate):
    pop = pop_entrada.copy()
    new_pop = []
    
    # Para termos a população constante, iteramos o tamanho da população divido por 2
    # já que em cada iteração são gerado 2 membros da nova geração
    half_pop = int(len(pop)/2)
    for _ in range(half_pop):
        selecteds = tournament_select_two(pop)

        child1, child2 = crossover(selecteds)
        
        child1 = mutation(child1, prob_mutate)
        child2 = mutation(child2, prob_mutate)

        child1 = turn_feasible(child1)  # tornar solução factível 
        child2 = turn_feasible(child2)

        new_pop.append(child1)  # adicionar child a nova população
        new_pop.append(child2)

    return new_pop


array_of_best_fitness = [] # vetor para armazenar o melhor fitness de cada geração
def inicializar():
    population = create_initial_population(array_of_genes, num_elem_pop)
    current_mutate_prob = initial_mutate_prob

    index_geracao_atual = 0
    iteracoes_sem_melhora = 0
    num_iteracoes_melhor_solucao = 0
    best_solution_global = None
    best_fitness_global = 99999999999
    best_solution_atual = None  
    best_fitness_atual = 99999999999

    execution_time = time.time()

    while True:
        population = create_new_population(population, current_mutate_prob)
        index_geracao_atual += 1
        best_fitness_atual = 99999999999
        best_solution_atual = None

        for solution in population:
            fit_value = fitness(solution)
            if fit_value < best_fitness_atual:
                best_fitness_atual = fit_value
                best_solution_atual = solution

        array_of_best_fitness.append(best_fitness_atual)
        
        if best_fitness_atual >= best_fitness_global:
            iteracoes_sem_melhora += 1
            current_mutate_prob += 0.01

        else:
            best_solution_global = best_solution_atual
            best_fitness_global = best_fitness_atual
            iteracoes_sem_melhora = 0
            num_iteracoes_melhor_solucao = index_geracao_atual
            current_mutate_prob = initial_mutate_prob
            time_to_best_solution = time.time() - start_time
        

        # Checar o tempo de execução para anteder a condição de parada
        execution_time = time.time()
        time_elapsed = execution_time - start_time
        if time_elapsed > time_to_execute:
            break


    print('-----------------------------------------------------------------------------')
    print(f'fitness melhor entre todas gerações:{fitness(best_solution_global)}, melhor fitness atual: {fitness(best_solution_atual)}')
    print(f'num de iterações: {index_geracao_atual}, iterações sem melhora:{iteracoes_sem_melhora}, iterações pra melhor solução: {num_iteracoes_melhor_solucao}, tempo de exc da melhor solução: {time_to_best_solution}')
    print('-----------------------------------------------------------------------------')

    return best_solution_global


best_reached_solution = inicializar()

# # # ----------------------------------------
end_time = time.time()
print("Tempo de execução:", end_time-start_time)
# # # ----------------------------------------

def route_demands(solution):
    rotas = solution.copy()
    demanda_rotas = []
    demanda = 0.0
    for gene in rotas:
        demanda += gene.demand
        if gene.id== 0 and demanda != 0:
            demanda_rotas.append(demanda)
            demanda = 0
    demanda_rotas.append(demanda)
    return demanda_rotas

def x_values(genes_list):
    list_x = []
    for gene in genes_list:
        list_x.append(gene.x)
    return list_x

def y_values(genes_list):
    list_y = []
    for gene in genes_list:
        list_y.append(gene.y)
    return list_y


plot_sol = best_reached_solution.copy()
plot_sol.insert(0,array_of_genes[0])
num_exato_rotas = plot_sol.count(array_of_genes[0])
plot_sol.append(array_of_genes[0])
if num_exato_rotas != k_rotas:
    print('NOT ENOUGH TIME TO FIND A FEASIBLE SOLUTION!')
    print('CURRENT SOLUTION PROBABLY USES MORE VEHICLES THAN THE MINIMUM POSSIBLE!')
    print('TRY RUNNING FOR A LONGER PERIOD OR WITH DIFFERENT PARAMETERS')


print(f'Número de Veículos utilizados: {num_exato_rotas}')
print(f'Número Mínimo de Veículos(rotas) possível: {k_rotas}')
print(f'Capacidade máxima do veículo: {k_cap_max}')
print(f'demanda das rotas {route_demands(best_reached_solution)}')
print(f'Número de cidades a serem atendidas: {n_genes}')
cities_sum_demands = sum([gene.demand for gene in array_of_genes])
print('demanda total das cidadeds:',cities_sum_demands)


# # # ----------- plot section---------------

plt.scatter(x_values(array_of_genes), y_values(
    array_of_genes), s=20, c='blue')
plt.scatter(array_of_genes[0].x, array_of_genes[0].y, s=35, c='black')

print(f'COST:{fitness(best_reached_solution)}, SOLUTION:')
print(plot_sol)
list_to_plot = []
for each in plot_sol:
    list_to_plot.append(each)
    if each.id == 0:
        list_to_plot.append(array_of_genes[0])
        plt.plot(x_values(list_to_plot),y_values(list_to_plot))
        list_to_plot.clear()
        list_to_plot.append(array_of_genes[0])

resformat = "{:.2f}".format(array_of_best_fitness[-1])
plt.legend(["cost: " + resformat], loc="upper right", )

plt.show()

# ### Grático para plotar extra A-n32...
# plt.xkcd()
# fitness_final = array_of_best_fitness[-1]
# # plt.grid()
# plt.ylim(fitness_final-250,fitness_final+250)
# stringBestcost = "Obtida: " + str("{:.2f}".format(array_of_best_fitness[-1]))
# plt.plot(array_of_best_fitness, color='g', label=stringBestcost)
# plt.axhline(y=784, color='b', linestyle='-', label="Melhor: 784")
# plt.legend(loc="upper right")
# plt.show()
