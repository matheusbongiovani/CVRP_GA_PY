import sys
import time
import random
import matplotlib.pyplot as plt

#Classe Cidade/Gene, que representa as cidades da instância.
class Cidade(object):
    def __init__(self, x=0.0, y=0.0, demand=0.0, id=0):
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


class Rotas(object):
    def __init__(self):
        self.k = 0
        self.cidades = []
        self.carga = 0
        self.cost = 0

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        rota_repr = 'k:' + str(self.k) + ', carga:' + str(self.carga) + ', custo:' + str(self.cost)
        return rota_repr

class Solution(object):
    def __init__(self):
        self.rotas = []
        self.fitness = 0

    def __str__(self):
        return str(self.fitness)

    def __repr__(self):
        return str(self.fitness)


start_time = time.time()

if len(sys.argv) != 4:
    print('----------------------ERROR----------------------')
    print('Sintaxe: python3 "program.py" "instância.vrp" "população" "prob mutação(%)" ')
    sys.exit('-------------------------------------------------')
else:
    arg1 = sys.argv[1]
    arg_size = sys.argv[2]
    arg_mutate = float(sys.argv[3])/100
    

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
                node = Cidade(float(split_id_XY[1]), float(
                    split_id_XY[2]), id=(int(split_id_XY[0])-1))
                array_of_genes.append(node)

        # trecho para inserir a demanda de cada nó no vetor array_of_genes
        if demand_section_bool:
            if linha.find('DEMAND_SECTION') != -1:
                continue
            if linha.find('DEPOT_SECTION') != -1:
                demand_section_bool = False
            else:
                splitDemand = linha.split()
                array_of_genes[index_entrada].demand = float(splitDemand[1])
                index_entrada += 1
# ---- fim da leitura da entrada ----


n_genes = index_entrada  # nº de cidades
k_rotas = header_array[0].split('-k') 
k_rotas = int(k_rotas[1]) # nº de veículos
k_cap_max = float(header_array[5]) # capacidade dos veículos

cidades_wout_depot = array_of_genes.copy()
cidades_wout_depot.pop(0)

array_of_rotas = []
for veiculo in range(k_rotas):
    veiculo = Rotas()
    array_of_rotas.append(veiculo)


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

def cost_of_route(route):
    cost = 0
    i = 0

    cost += matrix_distancias[0][route[0].id]  #1º nó da 1ª rota
    for _ in range(len(route)-1):
        cost += matrix_distancias[route[i].id][route[i+1].id]
        i += 1
    cost += matrix_distancias[route[i].id][0] #último nó da última rota

    return cost





def distribute_demand_to_routes(genes):
    # modelo entrada [1,2,3,4,5,6,7...n]
    randomized = random.sample(genes, len(genes))
    route_list = [[] for i in range(k_rotas)]
    rota_atual = 0
    for gene in randomized:
        if rota_atual == k_rotas:
            rota_atual = 0
        route_list[rota_atual].append(gene)
        rota_atual += 1

    carga_rota = 0
    carga_list = []
    for route in route_list:
        for cidade in route:
            carga_rota += cidade.demand
        carga_list.append(carga_rota)
        carga_rota = 0

    i = 0
    while i < k_rotas:
        array_of_rotas[i].k = i
        array_of_rotas[i].cidades = route_list[i]
        array_of_rotas[i].carga = carga_list[i]
        array_of_rotas[i].cost = cost_of_route(route_list[i])
        i += 1

    route_list = array_of_rotas.copy()

    return route_list

route_list = distribute_demand_to_routes(cidades_wout_depot)



# não dá pra tentar resolver isto na mão, tem q usar a metaheuristica...
def adjust_route(route_list_aux):
    route_list = route_list_aux.copy()
    sobrando = []
    excedido = []
    
    for rota in route_list:
        if rota.carga <= k_cap_max:
            sobrando.append(rota)
        if rota.carga > k_cap_max:
            excedido.append(rota)
    
    if len(excedido) == 0:
        return route_list
    
    for rota in excedido:
        while rota.carga > k_cap_max:
            ncidades = len(rota.cidades)
            index_random = random.randrange(ncidades)
            
            for elem in sobrando:
                if rota.cidades[index_random].demand + elem.carga <= k_cap_max:
                    removida = rota.cidades.pop(index_random)
                    rota.carga -= removida.demand
                    elem.cidades.append(removida)
                    elem.carga += removida.demand
                    elem.cost = cost_of_route(elem.cidades)
                    break
        rota.cost = cost_of_route(rota.cidades)

    # for each in sobrando:
    #     route_list.pop(each.k)
    #     route_list.insert(each.k,each)

    # for each in excedido:
    #     route_list.pop(each.k)
    #     route_list.insert(each.k,each)

    return route_list


eeeend = 0