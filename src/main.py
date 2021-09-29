import time
from datetime import datetime

class Node:
    """
    Classe que representa o no.
    """
    def __init__(self, state, goal, parent=None):
        """
        Metodo construtor da classe Node.
        """
        self.state = state
        self.neighbors = []
        self.visited_right = False
        self.visited_left = False
        self.parent_right = None
        self.parent_left = None
        self.parent = parent
        self.g = 0 if not parent else parent.g + 1
        self.h = self.get_h(goal)
        self.f = self.g + self.h
    
    def __repr__(self):
        """
        Sobrescrita do metodo __repr__ que representa a classe como uma string
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
    
    def __eq__(self, another_node):
        """
        Sobrescrita do metodo de igualdade (__eq__).
        """
        return Node.state_as_string(self.state) == Node.state_as_string(another_node.state)
    
    def get_h(self, goal):
        value_of_h = 0

        for index, value in enumerate(goal):
            if self.state[index] != value and value != 0:
                value_of_h += 1
        
        return value_of_h

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
    
    @staticmethod
    def state_as_string(state):
        """
        Metodo estatico que retorna o estado de um no como uma string.
        """
        new_state = [str(element) for element in state]

        return ''.join(new_state)

class Graph:
    """
    Classe que representa o grafo
    """
    def __init__(self, initial_state):
        """
        Metodo construtor da classe
        """
        self.initial_state = initial_state
        self.final_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        self.nodes = {}
        self.add_node(self.initial_state)
        self.add_node(self.final_state)
        self.results = []
    
    def add_result(self, method_name, method_time, path, visited_nodes):
        """
        Metodo que adiciona um resultado a lista de resultados
        """
        self.results.append(Result(method_name, method_time, path, visited_nodes))

    def add_node(self, state):
        """
        Metodo que adiciona um no ao grafo
        """
        state_as_string = Node.state_as_string(state)

        if not self.nodes.get(state_as_string):
            node = Node(state, self.final_state)

            self.nodes[state_as_string] = node

        return self.nodes.get(state_as_string)
    
    def add_edge(self, state1, state2):
        """
        Metodo que adiciona uma aresta ao no
        """
        state_1_as_string = Node.state_as_string(state1)

        state_2_as_string = Node.state_as_string(state2)

        if not (self.nodes.get(state_1_as_string) and self.nodes.get(state_2_as_string)):
            return False
        
        node_1 = self.nodes.get(state_1_as_string)

        node_2 = self.nodes.get(state_2_as_string)

        node_1.add_neighbor(node_2)

        node_2.add_neighbor(node_1)

        return True
    
    def get_neighbors(self, node):
        """
        Metodo que retorna os nos visinhos de um no
        """
        neighbors = []

        for state in node.neighboring_states():
            neighbor = self.get_node(state)

            if neighbor:
                neighbors.append(neighbor)
            else:
                neighbor = self.add_node(state)

                neighbors.append(neighbor)
        
        return neighbors
    
    def get_node(self, state):
        """
        Metodo que retorna um no do grafo
        """
        return self.nodes.get(Node.state_as_string(state))
    
    def is_intersecting(self, node):
        """
        Metodo auxiliar da busca bidirecional que verifica se o no e a intersecao da busca
        """
        return node.visited_left and node.visited_right
    
    def bidirectional_search(self):
        """
        Metodo que realiza a busca bidirecional e salva o resultado na lista de resultados
        """
        begin = time.time()

        initial_node = self.get_node(self.initial_state)

        final_node = self.get_node(self.final_state)

        queue = [initial_node, final_node]

        initial_node.visited_right = True
        
        final_node.visited_left = True

        visited_nodes = []
    
        while queue:
            node = queue.pop(0)

            if self.is_intersecting(node):
                end = time.time()

                method_time = end - begin

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

                self.add_result('Busca bidirecional', method_time, path, visited_nodes)
                
                return True
            else:
                states = node.neighboring_states()

                neighbors = [self.add_node(state) for state in states]

                for neighbor in neighbors:
                    if node.visited_left and not neighbor.visited_left:
                        neighbor.parent_left = node

                        neighbor.visited_left = True

                        queue.append(neighbor)
                        
                        visited_nodes.append(neighbor)

                    if node.visited_right and not neighbor.visited_right:
                        neighbor.parent_right = node

                        neighbor.visited_right = True

                        queue.append(neighbor)

                        visited_nodes.append(neighbor)
        
        end = time.time()

        method_time = end - begin

        self.add_result('Busca bidirecional', method_time, [], visited_nodes)

        return False
    
    def reset_graph(self):
        """
        Metodo que reinicializa o grafo
        """
        self.nodes = {}
        self.add_node(self.initial_state)
        self.add_node(self.final_state)

    def a_start(self):
        """
        Metodo que realiza a busca pelo metodo A-estrela e salva o resultado na lista de resultados
        """
        begin = time.time()

        self.reset_graph()

        border = []
        path = []

        visited_nodes = []

        border_size = 0

        initial_node = self.get_node(self.initial_state)

        final_node = self.get_node(self.final_state)

        border.append(initial_node)

        current = border.pop(0)

        while current and not current == final_node:
            neighbors = []

            for state in current.neighboring_states():
                neighbor = Node(state, self.final_state, current)

                neighbors.append(neighbor)
        
            for neighbor in neighbors:
                if not neighbor in border:
                    border.append(neighbor)

                    visited_nodes.append(neighbor)
            
            border.sort(key = lambda x: x.f)

            if border_size < len(border):
                border_size = len(border)
            
            current = border.pop(0)
        
        while current.parent is not None:
            path.insert(0, current)

            current = current.parent
        
        end = time.time()

        method_time = end - begin

        self.add_result('A-estrela', method_time, path, visited_nodes)
                
        return path

class Result:
    """
    Classe que representa o resultado da busca
    """
    def __init__(self, method_name, method_time, path, visited_nodes):
        """
        Metodo construtor da classe
        """
        self.name = method_name
        self.time = method_time
        self.path = path
        self.visited_nodes = visited_nodes
    
    def __repr__(self):
        """
        Sobrescrita do metodo __repr__ que representa a classe como uma string
        """
        result_as_string = f'Metodo: {self.name}\n'
        result_as_string += f'Tempo: {round(self.time, 6)} segundos\n'
        result_as_string += f'Quantidade de nos visitados: {len(self.visited_nodes) - 1 if self.name == "Busca bidirecional" else len(self.visited_nodes)}\n'
        result_as_string += f'Quantidade de jogadas: {len(self.path)}\n'
        result_as_string += f'Caminho das jogadas\n'

        for i in range(len(self.path)):
            result_as_string += f'Jogada {i + 1}\n' + str(self.path[i])

            if i < len(self.path) - 1:
                result_as_string += '\n'
        
        return result_as_string

def convert_string_in_numbers_array(input_as_string):
    input_as_array = input_as_string.split(' ')

    converted_input = []

    for element in input_as_array:
        try:
            converted_input.append(int(element))
        except:
            return False, []
        
    return True, converted_input

def user_input():
    validated_input = False

    initial = []

    while not validated_input:
        print('Entre com o estao inicial no seguinte formato:')
        print('Linha 1: 2 0 3')
        print('Linha 2: 1 7 4')
        print('Linha 3: 6 8 5')
        print()

        data1_as_string = input('Linha 1: ')
        data2_as_string = input('Linha 2: ')
        data3_as_string = input('Linha 3: ')
        print()

        all_int, data1_as_array = convert_string_in_numbers_array(data1_as_string)

        message_all_int = 'Todos numeros devem ser inteiros'

        if not all_int:
            print(message_all_int)
            continue

        all_int, data2_as_array = convert_string_in_numbers_array(data2_as_string)
        
        if not all_int:
            print(message_all_int)
            continue

        all_int, data3_as_array = convert_string_in_numbers_array(data3_as_string)

        if not all_int:
            print(message_all_int)
            continue

        duplicate = False

        for i in range(len(data1_as_array)):
            for j in range(len(data1_as_array)):
                for k in range(len(data1_as_array)):
                    if data1_as_array[i] == data2_as_array[j] or data2_as_array[j] == data3_as_array[k]:
                        duplicate = True
        
        if duplicate:
            print('Nao deve ter numeros duplicados')
            continue

        if len(data1_as_array) + len(data2_as_array) + len(data3_as_array) != 9:
            print('Deve ter 9 numeros')
            continue

        initial.extend(data1_as_array)

        initial.extend(data2_as_array)
        
        initial.extend(data3_as_array)

        out_of_range = False

        for element in initial:
            if not (element >= 0 and element <= 8):
                out_of_range = True

        if out_of_range:    
            initial = []
            
            print('Os numeros devem estar entre 0 e 8.')

            continue

        validated_input = True
    
    return initial

def main():
    initial = user_input()

    print(initial)

    graph = Graph(initial)

    print('Busca bidirecional iniciada')

    graph.bidirectional_search()

    print('Busca bidirecional finalizada')

    print('Busca a-estrela iniciada')
    
    graph.a_start()

    print('Busca a-estrela finalizada')

    time_result = datetime.now()

    best_result = None

    for element in graph.results:
        out_file = open(f'logs/{time_result}_{element.name}.log', 'wt')
        out_file.write(str(element))
        out_file.close()

        if not best_result:
            best_result = element
        else:
            best_result = best_result if len(best_result.path) < len(element.path) else element
    
    print(f'O melhor resultado foi do metodo {best_result.name} com duracao de {round(best_result.time, 6)} segundos')

main()    
