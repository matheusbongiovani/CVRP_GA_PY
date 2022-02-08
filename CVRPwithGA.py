import sys
import Node

if len(sys.argv) != 3:
    print('----------------------ERROR----------------------')
    print('Sintaxe: python3 "program" "instâncias" "solução" ')
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

        # trecho para pular linhas antes de armazenar a posição dos nós
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
                splitXY = linha.split()
                node = Node.Node(splitXY[1], splitXY[2])
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


# print(array_of_nodes[31])
# print(i)

def print_node_list(node_list):
    node_index = 1
    for node in node_list:
        print('node:' + str(node_index) + ' <' + str(node.getX()) + ',' +
              str(node.getY()) + ',' + str(node.getZ()) + '>')
        node_index += 1


print_node_list(array_of_nodes)
