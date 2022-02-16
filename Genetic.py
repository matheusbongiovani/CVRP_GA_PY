import random
import time

# ------------------ Genetic Algorithm
# Gene: Corresponde a uma cidade, contendo as cordenadas X,Y e demanda
# Subcromo: Corresponde a uma rota, feita por um veículo, contendo conjunto de Genes
# -- Subcromo: [gene1, gene2, gene3] representando 1tour (rota feita por 1 veículo)
# Cromossomo: Correseponde ao conjunto de tours feito por todos os veículos (solução do problema)
# -- solution_cromos: [[gene1, gene2, gene3], [gene7, gene4, gene5], [gene8, gene6, gene9]] (0,2,1,3,0,7,4,5,0,8,6,9,0)
# População: Conjunto de solution_cromos


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

