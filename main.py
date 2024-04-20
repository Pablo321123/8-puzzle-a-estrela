import copy


class Tabuleiro:
    def __init__(self, table=[[7, 2, 4], [5, 0, 6], [8, 3, 1]]) -> None:
        self.table = table
        self.resolved = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    def __eq__(self, table) -> bool:  # Verifico se o tabuleiro é igual a solucao
        return self.resolved == table

    def __str__(self) -> str:
        # textoTabuleiro = f"{self.table[0]}\n{self.table[1]}\n{self.table[2]}\n\nGoal\n{self.resolved[0]}\n{self.resolved[1]}\n{self.resolved[2]}\n"
        textoTabuleiro = f"{self.table[0]}\n{self.table[1]}\n{self.table[2]}\n"
        return textoTabuleiro

    # busco pela posicao atual do branco (mas, consigo pesquisar por algum outro tambem, caso nescessario)
    # Point aqui, diz respeito ao 'tabuleiro' na qual queremos encontrar um elemento
    def searchPoint(self, point, element=0):
        for i in range(len(self.table[0])):
            for j in range(len(self.table)):
                if point[i][j] == element:
                    return i, j  # linha, coluna

    def mahatanDistance(
        self, element1, currentPoint
    ):  # CurrentPoint é o tabuleiro atual
        md = 0
        linhaGoal, colunaGoal = self.searchPoint(self.resolved, element1)
        linha, coluna = self.searchPoint(currentPoint, element1)
        md = abs(linhaGoal - linha) + abs(colunaGoal - coluna)
        print(f"Distance of {element1}: {md}")
        return md

    def getTable(self):
        return self.table

    def getResolved(self):
        return self.resolved

    # Profundidade = g
    def moveUp(self, height, currentNode):
        newTable = copy.deepcopy(self.table)
        tableParent = (
            currentNode.parent.point.table if currentNode.parent is not None else []
        )

        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if newTable[i][j] == 0:
                    if i - 1 < 0:
                        return False
                    else:
                        h = self.mahatanDistance(self.table[i - 1][j], newTable)
                        newTable[i - 1][j] = 0
                        newTable[i][j] = self.table[i - 1][j]
                        if newTable == tableParent:
                            return False
                        return Node(Tabuleiro(newTable), currentNode, h, height + 1)
        return newTable

    def moveRight(self, height, currentNode):
        newTable = copy.deepcopy(self.table)
        tableParent = (
            currentNode.parent.point.table if currentNode.parent is not None else []
        )

        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if newTable[i][j] == 0:
                    if j + 1 > 2:
                        return False
                    else:
                        h = self.mahatanDistance(self.table[i][j + 1], newTable)
                        newTable[i][j + 1] = 0
                        newTable[i][j] = self.table[i][j + 1]
                        if newTable == tableParent:
                            return False
                        return Node(Tabuleiro(newTable), currentNode, h, height + 1)
        return newTable

    def moveDown(self, height, currentNode):
        newTable = copy.deepcopy(self.table)
        tableParent = (
            currentNode.parent.point.table if currentNode.parent is not None else []
        )

        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if newTable[i][j] == 0:
                    if i + 1 > 2:
                        return False
                    else:
                        h = self.mahatanDistance(self.table[i + 1][j], newTable)
                        newTable[i + 1][j] = 0
                        newTable[i][j] = self.table[i + 1][j]

                        if newTable == tableParent:
                            return False

                        return Node(Tabuleiro(newTable), currentNode, h, height + 1)
        return newTable

    def moveLeft(self, height, currentNode):
        newTable = copy.deepcopy(self.table)
        tableParent = (
            currentNode.parent.point.table if currentNode.parent is not None else []
        )

        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if newTable[i][j] == 0:
                    if j - 1 < 0:
                        return False
                    else:
                        h = self.mahatanDistance(self.table[i][j - 1], newTable)
                        newTable[i][j - 1] = 0
                        newTable[i][j] = self.table[i][j - 1]
                        if newTable == tableParent:
                            return False
                        return Node(Tabuleiro(newTable), currentNode, h, height + 1)
        return newTable


class Node:
    def __init__(self, point: Tabuleiro, parent: Tabuleiro, h, g=0) -> None:
        self.point = point
        self.parent = parent
        self.h = h
        self.g = g  # O custo será a profundidade da árvore
        self.f = 0

    def __eq__(self, point) -> bool:
        return self.point == point

    def __str__(self) -> str:
        return f"Point: {self.point}\nParent: {self.parent}\nH: {self.h}\nG: {self.g}"

    def addNode(self, point, parent, h, g=0):
        return Node(point, parent, h, g)

    def getPoint(self):
        return self.point


class EstrelaA:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.startSolution(self.node)  # , self.node.point.getResolved()

    def verifyNodeExists(self, lstNodes, currentNode):
        if not currentNode:
            return False
        for op in lstNodes:
            op: Node
            if (
                op.point.table == currentNode.point.table
                and op.parent.point.table == currentNode.parent.point.table
            ):
                return False

        return True

    def startSolution(self, startNode: Node):
        currentNode: Node = startNode
        currentTable: Tabuleiro = self.node.point
        nextTable: Tabuleiro = None
        lstOptions = []

        # Verifica se o currentNode é igual a solução
        while not (currentTable == nextTable):
            # print(currentNode.moveUp())

            # Testar as 4 direções
            g_depth = currentNode.parent.g if currentNode.parent is not None else 0

            mup = currentTable.moveUp(g_depth, currentNode)
            mr = currentTable.moveRight(g_depth, currentNode)
            mb = currentTable.moveDown(g_depth, currentNode)
            ml = currentTable.moveLeft(g_depth, currentNode)

            if len(lstOptions) == 0:
                lstOptions.append(mup)
                lstOptions.append(mr)
                lstOptions.append(mb)
                lstOptions.append(ml)
            else:
                if self.verifyNodeExists(lstOptions, mup):
                    lstOptions.append(mup)

                if self.verifyNodeExists(lstOptions, mr):
                    lstOptions.append(mr)

                if self.verifyNodeExists(lstOptions, mb):
                    lstOptions.append(mb)

                if self.verifyNodeExists(lstOptions, ml):
                    lstOptions.append(ml)

            lstOptions = list(filter(bool, lstOptions))

            # Calculo o valor de F para cada Nó
            for node in lstOptions:
                node: Node
                if node.f == 0:
                    node.f = self.calc_g_amount(node) + node.h

            # Pego o menor valor de F dentre os nós espandidos
            min_table = min(lstOptions, key=lambda x: x.f)
            currentNode = min_table
            currentTable = currentNode.getPoint()

            print(currentTable)

            lstOptions.remove(min_table)

    def calc_g_amount(self, node: Node):
        g_amount = 0
        current_edge = node

        while current_edge.parent != None:
            g_amount += current_edge.g
            current_edge = current_edge.parent

        return g_amount

    def showOptions(self, g_options_all):
        for o in g_options_all:
            print(f"{o[0].origem} --{o[1]}--> {o[0].destino}")

    def startSearch(self, source, destiny):
        n = 0
        current_table = source
        # current_edge = Edge()
        lastCity = ""
        g_options_all = []  # nome f g_accumulate
        path = []

        while True:
            print(
                "\n---------------------------------------------------------------------------\n"
                f"PASSO: {n}"
                "\n---------------------------------------------------------------------------\n"
            )
            n += 1

            if current_table == destiny:
                path = current_edge
                break

            # nextCity[3]: g_accumulate, nextCity[2]: valor de h, nextCity[1]:  custo g, nextCity[0]: nome destino
            for nextCity in self.grafo[current_table]:
                nextCity: Edge

                if nextCity.destino in nextCity.path:
                    continue

                g_accumulate = self.calc_g_amount(nextCity)

                custoTotal = nextCity.g_distancia + g_accumulate
                f = custoTotal + nextCity.h_destino

                nextCity.path.append(nextCity.origem)

                # Verifico se já não tem uma opção ou se uma opção já foi visitada
                g_options_all.append([nextCity, f])

            # min_result = min(g_options_all, key=lambda x: x[1])
            self.showOptions(g_options_all)

            lastCity = current_table
            print(f"Origem: {lastCity}")

            cityBestCost = min(g_options_all, key=lambda x: x[1])
            current_table = cityBestCost[0].destino
            current_edge = cityBestCost[0]

            if len(g_options_all) > 0:
                indexCityChoice = [
                    indice
                    for indice, city in enumerate(g_options_all)
                    if city[0] == current_edge
                ]
                g_options_all.pop(indexCityChoice[0])

            print(f"city escolhida: {current_table}")
            for c in self.grafo[current_table]:
                c.path = (
                    current_edge.path.copy()
                )  # Ele tava compartilhando o mesmo local de memoria

        print(
            "\n---------------------------------------------------------------------------\n"
            f"Melhor Caminho: {path.path} -> {path.destino}\n"
            f"Custo Total: {self.calc_g_amount(nextCity) + path.g_distancia}"
            "\n---------------------------------------------------------------------------\n"
        )


table = Tabuleiro()
parentNode = Node(
    table, None, 0, 0
)  # h == 0 aqui porque o branco, na realidade não tem um lugar em si para ele, o lugar dele vai depender de como é a matriz objetivo

busca = EstrelaA(parentNode)


# print(table)
# table2 = Tabuleiro(table.moveLeft())
# print(table2)
# print(table.mahatanDistance(1, table.getTable()))

# print(f"\nMoveUp:\n{table.moveUp()}\n")


# caminho = EstrelaA(grafo.getGrafo())
# print("Busca Concluida!")