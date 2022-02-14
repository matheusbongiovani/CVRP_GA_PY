import sys
import Gene
import matplotlib.pyplot as plt
import numpy as np


# cada meta-heurística possui um conjunto de parâmetros cujos
# valores devem ser fornecidos pela entrada
if len(sys.argv) != 3:
    print('----------------------ERROR----------------------')
    print('Sintaxe: python3 "program.py" "instância.vrp" "solução" ')
    sys.exit('-------------------------------------------------')
else:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

i = 0
header_array = []
array_of_nodes = []

with open(arg1, mode='r', encoding='utf-8') as file:
    # file.read()
    # print(file.read())

    num_linha = 0
    node_coord_bool = False
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
                node_coord_bool = True

        # trecho para armazenar as posições no vetor array_of_nodes
        if node_coord_bool:
            if linha.find('DEMAND_SECTION') != -1:
                node_coord_bool = False
                demand_section_bool = True

            else:
                split_id_XY = linha.split()
                node = Gene.Gene(float(split_id_XY[1]), float(
                    split_id_XY[2]), id=int(split_id_XY[0]))
                array_of_nodes.append(node)

        # trecho para inserir a demanda de cada nó no vetor array_of_nodes
        if demand_section_bool:
            if linha.find('DEMAND_SECTION') != -1:
                continue
            if linha.find('DEPOT_SECTION') != -1:
                demand_section_bool = False
            else:
                splitZ = linha.split()
                array_of_nodes[i].z = splitZ[1]
                i += 1

# O Depot sempre será o 1º elemento e com demanda 0 (node: 0 <82,76,0>)
n_numero_de_cidades = i

# obter valor K, que representa o número de veículos dado pela entrada
k_numero_de_veiculos = header_array[0].split('-k')
k_numero_de_veiculos = k_numero_de_veiculos[1]

Q_capacidade_maxima_veiculo = header_array[5]

print(f'Número de cidades a serem atendidas: {n_numero_de_cidades}')
print(f'Número de Veículos (número de rotas): {k_numero_de_veiculos}')
print(f'Capacidade máxima do veículo: {Q_capacidade_maxima_veiculo}')


def print_node_list(node_list):
    for node in node_list:
        print(node.__str__())


def x_values(node_list):
    list_x = []
    for node in node_list:
        list_x.append(node.getX())
    return list_x


def y_values(node_list):
    list_y = []
    for node in node_list:
        list_y.append(node.getY())
    return list_y


def total_demand(node_list):
    total_demand = 0
    for node in node_list:
        total_demand += float(node.getZ())
    return total_demand


print_node_list(array_of_nodes)

# print(total_demand(array_of_nodes))

# plt.xkcd()  # deixar visual de quadrinho
plt.grid(True)
plt.scatter(x_values(array_of_nodes), y_values(
    array_of_nodes), s=20, c='blue')
plt.scatter(array_of_nodes[0].x, array_of_nodes[0].y, s=30, c='red')

plt.show()
