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
with open(arg1, mode='r', encoding='utf-8') as file:
    # file.read()
    # print(file.read())

    num_linha = 0
    header_array = []
    node_coord_bool = False
    demand_section_bool = False
    node_coord_tuples_array = []

    for linha in file:
        # print(line, end='')

        if num_linha < 6:
            num_linha += 1
            splited = linha.split()
            header_array.append(splited[2])

        # if linha.find('NODE_COORD_SECTION') != -1:
        if num_linha >= 6 and num_linha < 9:
            num_linha += 1
            if num_linha > 8:
                node_coord_bool = True

        if node_coord_bool:
            if linha.find('DEMAND_SECTION') != -1:
                node_coord_bool = False
                demand_section_bool = True

            else:
                splitXY = linha.split()
                node = Node.Node(splitXY[1], splitXY[2])
                node_coord_tuples_array.append(node)

        if demand_section_bool:
            if linha.find('DEMAND_SECTION') != -1:
                continue
            if linha.find('DEPOT_SECTION') != -1:
                demand_section_bool = False
            else:
                splitZ = linha.split()
                node_coord_tuples_array[i].z = splitZ[1]
                i += 1

print(node_coord_tuples_array[31])
print(i)
