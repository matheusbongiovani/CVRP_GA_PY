import random
import time

# ------------------ Genetic Algorithm
# Gene: Corresponde a uma cidade, contendo as cordenadas X,Y e demanda
# Cromossomo: Corresponde a uma rota, feita por um veículo, contendo conjunto de Genes
# -- cromo: [gene1, gene2, gene3] representando 1tour (rota feita por 1 veículo)
# Solution_cromos: Correseponde ao conjunto de tours feito por todos os veículos (solução do problema)
# -- solution_cromos: [[gene1, gene2, gene3], [gene7, gene4, gene5], [gene8, gene6, gene9]] (0,2,1,3,0,7,4,5,0,8,6,9,0)
# População: Conjunto de solution_cromos


class Gene(object):

    def __init__(self, x=0, y=0, z=0, id=0):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

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


# c0 = Node(0, 0)
# c1 = Node(-1, -1)
# c2 = Node(2, 2)
# print(c1.distance(c2))
# print(c1.distance_from_origin())
# print(c1)
# print(c2)
# print(c1 == c2)


class Cromossomo(object):

    def __init__(self, k=0):
        self.k = k  # representa o nº do veículo 'k'
        self.tour_genes = []
        self.fitness = 0  # distância total do tour. Menor = melhor
        self.total_demand = 0

    def setK(self, k):
        self.k = k

    def getK(self):
        return int(self.k)

    def tour_add_gene(self, gene):
        self.tour_genes.append(gene)

    def remove_gene_at_index(self, index=-1):
        return self.tour_genes.pop(index)

    def remove_especific_gene(self, gene):
        self.tour_genes.remove(gene)

    def tour_total_demand(self):
        for gene in self.tour_genes:
            self.total_demand += gene.getZ()
        return self.total_demand

    def tour_fitness_wout_depot(self):
        gen_list = []
        number_of_genes = 0
        gen_index = 0
        total_distance = 0
        for gene in self.tour_genes:
            gen_list.append(gene)
            number_of_genes += 1
        for _ in range(number_of_genes - 1):
            total_distance += gen_list[gen_index].distance(gen_list[gen_index +
                                                                    1])
            gen_index += 1

        return total_distance

    def tour_fitness_with_depot(self, depot_node):
        dist_depot_to_first = depot_node.distance(self.tour_genes[0])
        dist_intermed = Cromossomo.tour_fitness_wout_depot(self)
        dist_depot_to_last = depot_node.distance(self.tour_genes[-1])
        return (dist_depot_to_first + dist_intermed + dist_depot_to_last)

    def __eq__(self, other):
        return self.tour_genes == other.set_of_genes


class Solution_cromos(object):
    def __init__(self):
        self.conjunto_k = set()
        self.cromos_in = []
        sol_fitness = 0

    def add_cromo_to_sol(self, cromo):
        if cromo.getK not in self.conjunto_k:
            self.cromos_in.append(cromo)
            self.conjunto_k.add(cromo.getK)

    def solution_fitness(self):
        pass


class Population_set(object):

    def __init__(self, size):
        self.size = size
        self.cromos_list = []

    def distribuir_genes_em_rotas(self, array_of_genes, num_k, cap_k):
        cromos_list = []
        cap_ocupada = 0
        index = 0
        current_k = 0
        randomized_list = random.sample(array_of_genes)

        for gene in array_of_genes:
            if cromos_list[index].tour_total_demand() + gene.getZ() < cap_k:
                cromos_list[index].append(gene)
            else:
                cromos_list[index].setK(current_k)
                current_k += 1
