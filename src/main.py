import time

class Node:
    """
    Classe que representa o no.
    """
    def __init__(self, state):
        """
        Metodo construtor da classe Node.
        """
        self.state = state
        self.neighbors = []
        self.visited_right = False
        self.visited_left = False
        self.parent_right = None
        self.parent_left = None
    
    def add_neighbor(self, node):
        """
        Metodo que adiciona um node adjacente.
        """
        self.neighbors.append(node)
    
    def neighboring_states(self):
        """
        Metodo que retorna os estados dos nos vizinhos. Dessa forma os nos sao criados no momento da execusao do algoritmo, otimizando a busca.
        """
        index = self.state.index(0)

        if index == 0:
            return [self.move(movement) for movement in ['down', 'right']]
        elif index == 1:
            return [self.move(movement) for movement in ['down', 'left', 'right']]
        elif index == 2:
            return [self.move(movement) for movement in ['down', 'left']]
        elif index == 3:
            return [self.move(movement) for movement in ['up', 'down', 'right']]
        elif index == 4:
            return [self.move(movement) for movement in ['up', 'down', 'left', 'right']]
        elif index == 5:
            return [self.move(movement) for movement in ['up', 'down', 'left']]
        elif index == 6:
            return [self.move(movement) for movement in ['up', 'right']]
        elif index == 7:
            return [self.move(movement) for movement in ['up', 'left', 'right']]
        else:
            # index == 8
            return [self.move(movement) for movement in ['up', 'left']]
    
    def state_as_string(self):
        """
        Metodo que retorna o estado do no como uma string.
        """
        new_state = [str(element) for element in self.state]

        return ''.join(new_state)
    
    def __repr__(self):
        """
        Sobrescrita do metodo __repr__.
        """
        representantion = ''

        for i in range(3):
            for j in range(3):
                representantion += str(self.state[3 * i + j])

                if j == 2 and i != 2:
                    representantion += '\n'
                else:
                    representantion += ' '

        return representantion
    
    def move(self, movement):
        """
        Metodo que retorna o estado apos o movimento.
        """
        index = self.state.index(0)

        new_state = self.state.copy()

        if movement == 'up':
            new_state[index], new_state[index - 3] = new_state[index - 3], new_state[index]
        elif movement == 'down':
            new_state[index], new_state[index + 3] = new_state[index + 3], new_state[index]
        elif movement == 'left':
            new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
        else:
            # movement == 'right'
            new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
        
        return new_state

class Graph:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.final_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        self.nodes = {}
        self.add_node(self.initial_state)
        self.add_node(self.final_state)

    def state_as_string(self, state):
        new_state = [str(element) for element in state]

        return ''.join(new_state)
    
    def add_node(self, state):
        state_as_string = self.state_as_string(state)

        if not self.nodes.get(state_as_string):
            node = Node(state)

            self.nodes[state_as_string] = node

        return self.nodes.get(state_as_string)
    
    def add_edge(self, state1, state2):
        state_1_as_string = self.state_as_string(state1)

        state_2_as_string = self.state_as_string(state2)

        if not (self.nodes.get(state_1_as_string) and self.nodes.get(state_2_as_string)):
            return False
        
        node_1 = self.nodes.get(state_1_as_string)

        node_2 = self.nodes.get(state_2_as_string)

        node_1.add_neighbor(node_2)

        node_2.add_neighbor(node_1)

        return True
    
    def get_node(self, state):
        return self.nodes.get(self.state_as_string(state))
    
    def is_intersecting(self, node):
        return node.visited_left and node.visited_right
    
    def bidirectional_search(self):
        print('Busca bidirecional inicializada')

        begin = time.time()

        initial_node = self.get_node(self.initial_state)

        final_node = self.get_node(self.final_state)

        queue = [initial_node, final_node]

        initial_node.visited_right = True
        
        final_node.visited_left = True
    
        while queue:
            node = queue.pop(0)

            if self.is_intersecting(node):
                end = time.time()

                print(f'Busca bidirecional finalizada com sucesso em {round(end - begin, 6)} segundos')
                
                return self.get_path(node)
            else:
                states = node.neighboring_states()

                neighbors = [self.add_node(state) for state in states]

                for neighbor in neighbors:

                    if node.visited_left and not neighbor.visited_left:
                        neighbor.parent_left = node
                        neighbor.visited_left = True
                        queue.append(neighbor)

                    if node.visited_right and not neighbor.visited_right:
                        neighbor.parent_right = node
                        neighbor.visited_right = True
                        queue.append(neighbor)
        
        print(f'Busca bidirecional finalizada sem encontrar um caminho em {round(end - begin, 6)} segundos')
        
    def get_path(self, node):
        copy_node = node

        path = []

        while node:
            path.append(node)

            node = node.parent_right

        path.reverse()

        del path[-1]

        while copy_node:
            path.append(copy_node)

            copy_node = copy_node.parent_left
        
        path_as_string = 'Caminho das jogadas\n#####\n'

        for i in range(len(path)):
            path_as_string += f'Jogada {i + 1}\n' + str(path[i])

            if i < len(path) - 1:
                path_as_string += '\n#####\n'
        
        return path_as_string
    
graph = Graph([2, 0, 3, 1, 7, 4, 6, 8, 5])

print(graph.bidirectional_search())

        
