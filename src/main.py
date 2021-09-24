from collections import deque

class Node:
    def __init__(self, state, color='white', parent=None):
        self.state = state
        self.parent = parent
        self.color = color
        self.adjacent = []
    
    def add_adjacent(self, node):
        self.adjacent.append(node)
    
    # Funcao que retorna os estados vizinhos
    def neighboring_states(self):
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
        new_state = [str(element) for element in self.state]

        return ''.join(new_state)
    
    def __repr__(self):
        representantion = ''

        for i in range(3):
            for j in range(3):
                representantion += str(self.state[3 * i + j])

                if j == 2 and i != 2:
                    representantion += '\n'
                else:
                    representantion += ' '

        return representantion
    
    # Funcao que retornar o estado apos o movimento
    def move(self, movement):
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

    def state_as_string(self, state):
        new_state = [str(element) for element in state]

        return ''.join(new_state)
    
    def add_node(self, state):
        state_as_string = self.state_as_string(state)

        if self.nodes.get(state_as_string):
            return self.nodes.get(state_as_string)
        else:
            node = Node(state)

            self.nodes[state_as_string] = node

            return node
    
    def add_edge(self, state1, state2):
        state_1_as_string = self.state_as_string(state1)

        state_2_as_string = self.state_as_string(state2)

        if not (self.nodes.get(state_1_as_string) and self.nodes.get(state_2_as_string)):
            return False
        
        node_1 = self.nodes.get(state_1_as_string)

        node_2 = self.nodes.get(state_2_as_string)

        node_1.add_adjacent(node_2)

        node_2.add_adjacent(node_1)

        return True
    
    def is_intersecting(self, node1, node2):
        return self.state_as_string(node1.next.state) == self.state_as_string(node2) and self.state_as_string(node2.next.state) == self.state_as_string(node1)
    
    def bidirectional_search(self):
        initial_node = self.nodes(self.initial_state)

        final_node = self.nodes(self.final_state)

        self.breadth_first_search(initial_node)

        self.breadth_first_search(final_node)

    def breadth_first_search(self, node):
        has_intersecting = False

        root = node

        root.color = 'gray'

        q = deque()
    
        q.append(root)

        while len(q) > 0 and not has_intersecting:
            u = q.popleft()

            states = u.neighboring_states()

            adjacent = [self.add_node(state) for state in states]

            for adjacent_node in adjacent:
                self.add_edge(u, adjacent_node)
            
            for adjacent_node in adjacent:
                if adjacent_node.color == 'white':
                    adjacent_node.color = 'gray'
                    adjacent_node.parent = u

                    q.append(adjacent_node)

            u.color = 'black'
    
node = Node([1, 2, 3, 8, 0, 4, 7, 6, 5])

print(node.neighboring_states())

print(node)
print(node.state_as_string())

        
