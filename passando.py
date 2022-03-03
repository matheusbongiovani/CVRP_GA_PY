import sys
import time
import random
import matplotlib.pyplot as plt


# Classe Gene, que representa as cidades da instância.
class Gene(object):
    def __init__(self, id=0, x=0, y=0, demand=0):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand

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

# leitura dos argumentos do terminal
if len(sys.argv) != 2:
    print('----------------------ERROR----------------------')
    print('Sintaxe: python3 "program.py" "instância.vrp"')
    sys.exit('-------------------------------------------------')
else:
    arg_entrada = sys.argv[1]

# leitura do arquivo de entrada:
header_array = []
array_of_genes = []
index_entrada = 0
with open(arg_entrada, mode='r', encoding='utf-8') as file:
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
                id, x, y = linha.split()
                node = Gene(int(id) - 1, float(x), float(y))
                array_of_genes.append(node)

        # trecho para inserir a demanda de cada nó no vetor array_of_genes
        if demand_section_bool:
            if linha.find('DEMAND_SECTION') != -1:
                continue
            if linha.find('DEPOT_SECTION') != -1:
                demand_section_bool = False
            else:
                _, demand = linha.split()
                array_of_genes[index_entrada].demand = float(demand)
                index_entrada += 1
# ---- fim da leitura da entrada ----

num_genes = len(array_of_genes) 
num_elem_pop = (num_genes-1) * 2  # nº elementos na população = nºcidades-depot * 2

# k_rotas: nº de veículos passado pela entrada
k_rotas = header_array[0].split('-k') # "NAME:B-n78" -k "10"
k_rotas = int(k_rotas[1]) # "10"

k_cap_max = float(header_array[5]) # capacidade máx dos veículos

time_to_execute = 60   # Tempo de execução do algoritmo em segundos

mutate_prob = 0.05


def func_matrix_distancias(genes):
    matrix_ij = []
    size = len(genes)
    for i in range(size):
        distancia = []
        for j in range(size):
            distancia.append(genes[i].distance(genes[j]))
        matrix_ij.append(distancia)
    return matrix_ij

matrix_distancias = func_matrix_distancias(array_of_genes)

def fitness(solution):
    cost = 0
    i = 0

    cost += matrix_distancias[0][solution[0].id]  #1º nó da 1ª rota
    for _ in range(len(solution)-1):
        cost += matrix_distancias[solution[i].id][solution[i+1].id]
        i += 1
    cost += matrix_distancias[solution[i].id][0] #último nó da última rota

    num_rotas_solucao = solution.count(array_of_genes[0])
    
    if num_rotas_solucao != k_rotas-1:
        weight = 0
        penalty = 0
        for cidade in solution:
            weight += cidade.demand
            if cidade.demand == 0:
                if weight > k_cap_max:
                    # penalty*50 performed better
                    penalty += (weight - k_cap_max)*50
                    cost += penalty
                    weight = 0

    # resultado = solution.copy()
    # resultado = solution.append(cost)

    return cost




def turn_feasible(cromo_entrada):
    genes_seq_entrada = array_of_genes.copy()
    genes_seq_entrada.pop(0)  # array com todas as cidades exceto o depot
    cromo = cromo_entrada.copy()
        
    cromo = [c for c in cromo if c.id != 0]
    
    # Trecho para remover eventuais cidades duplicadas e faltando, devido as mutações/crossOver
    adjust = True
    while adjust:
        adjust = False
        for i1 in range(len(cromo)):
            for i2 in range(i1):
                if cromo[i1] == cromo[i2]:
                    del_duplicated = True
                    for gene in genes_seq_entrada:
                        if gene not in cromo:
                            cromo[i1] = gene # cromo[i] recebe cidade(gene) 
                            del_duplicated = False # substitui cidade duplicada pela que esta faltando.
                            break
                    if del_duplicated:
                        del cromo[i1]
                    adjust = True
                if adjust: break
            if adjust: break

    # separar cidades em rotas # mudar jeito de como distribuir a demanda...
    total = 0.0
    i = 0   
    while i < len(cromo):
        total += cromo[i].demand  #Se demanda de i exceder, o Depot é inserido imediatamente antes
        if total > k_cap_max:
            cromo.insert(i, array_of_genes[0])
            total = 0
        i += 1
        
        
    return cromo



array_of_best_fitness = [] # vetor para armazenar o melhor fitness de cada geração
def inicializar():
    population = create_initial_population(array_of_genes, num_elem_pop)

    index_geracao_atual = 0
    iteracoes_sem_melhora = 0
    num_iteracoes_melhor_solucao = 0
    best_solution_global = None
    best_fitness_global = 99999999999
    best_solution_atual = None  
    best_fitness_atual = 99999999999

    execution_time = time.time()

    while True:
        population = create_new_population(population)
        index_geracao_atual += 1
        best_fitness_atual = 99999999999
        best_solution_atual = None

        # Passar a salvar custo das iterações (best fitness) para gerar gráficos
        for solution in population:
            fit_value = fitness(solution)
            if fit_value < best_fitness_atual:
                best_fitness_atual = fit_value
                best_solution_atual = solution
        
        array_of_best_fitness.append(best_fitness_atual)

        if best_fitness_atual >= best_fitness_global:
            iteracoes_sem_melhora += 1
            mutate_prob += 0.01
        else:
            best_solution_global = best_solution_atual
            best_fitness_global = best_fitness_atual
            num_iteracoes_melhor_solucao = index_geracao_atual
            time_to_best_solution = time.time() - start_time
            iteracoes_sem_melhora = 0
            mutate_prob = 0.05

        # se tiver 100 iterações sem melhora, reseta prob. de mutação
        if iteracoes_sem_melhora > 100:
            mutate_prob = 0.05

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


##---------------------------Report Section------------------------

plot_sol = best_reached_solution.copy()
plot_sol.insert(0,array_of_genes[0])
num_veiculos_usados_na_solucao = plot_sol.count(array_of_genes[0])
plot_sol.append(array_of_genes[0])

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


if num_veiculos_usados_na_solucao != k_rotas:
    print('NOT ENOUGH TIME TO FIND A FEASIBLE SOLUTION!')
    print('CURRENT SOLUTION PROBABLY USES MORE VEHICLES THAN THE MINIMUM POSSIBLE!')
    print('THIS INSTANCE MIGHT REQUIRE A LONGER COMPUTATIONAL TIME')

print(f'num of vehicles used in solution: {num_veiculos_usados_na_solucao}')
print(f'Número mínimo de veículos(rotas): {k_rotas}')
print(f'Capacidade máxima do veículo: {k_cap_max}')
print(f'Demanda das rotas {route_demands(best_reached_solution)}')
cities_sum_demands = sum([gene.demand for gene in array_of_genes])
print(f'Demanda total das cidades: {cities_sum_demands}')

# # # ----------- plot section---------------

x_gene_list = [gene.x for gene in array_of_genes]
y_gene_list = [gene.y for gene in array_of_genes]

plt.scatter(x_gene_list, y_gene_list, s=20, c='blue')
plt.scatter(array_of_genes[0].x, array_of_genes[0].y, s=35, c='red')

print(f'COST:{fitness(best_reached_solution)}, SOLUTION:')
print(plot_sol)
list_to_plot = []
for each in plot_sol:
    list_to_plot.append(each)
    if each.id == 0:
        list_to_plot.append(array_of_genes[0])
        x_list = [gene.x for gene in list_to_plot]
        y_list = [gene.y for gene in list_to_plot]   
        plt.plot(x_list, y_list)
        list_to_plot.clear()
        list_to_plot.append(array_of_genes[0])
plt.show()