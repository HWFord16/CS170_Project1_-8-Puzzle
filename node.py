class Node:
    def __init__(self, state, depth, move = None, parent = None, goal_state = [[1,2,3],[4,5,6],[7,8,0]]):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.goal_state = goal_state

        # G(n) = depth of state
        self.g = depth

        # h(n) = 0
        self.h = lambda x: 0

    # heuristic is just G(n) + h(n)
    def heuristic(self): return self.g + self.h(self.state)

    def add_child(self, child_node): self.children.append(child_node)

    def misplaced_tiles(self):
        if self.goal_state is None:  #Check node instance for goal_state
            return float('inf')

        #use numpy array ops. on elements for efficiency
        current_state = np.array(self.state)
        goal_state = np.array(self.goal_state)

        #find non-matching elements between states and return sum
        count = np.sum(current_state != goal_state)
        return count

    def euclidean(self):
        if self.goal_state is None:  ##Check node instance for goal_state
            return float('inf')

        #map the goal positions within 3x3 matrix
        goal_dict = dict()
        for i in range(3):
          for j in range(3):
            position = (i*3)+j+1
            if position < 9:      #for 9th element, keep but dont map position due to key errors
              goal_dict[position] = (i, j)

        #Lp distance function
        D = lambda x, y, p: sum( [ (abs(x[i]-y[i]) ** p) for i in range(len(x))] ) ** (1/p)

        #calculate total cost
        cost = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
              cell = self.state[i][j]
              if (cell != 0) and (cell in goal_dict): #dont calculate distance for blank element
                cost += D((i, j), goal_dict[cell], 2)

        return cost

    def expand(self):
        #Find the blank space == (0) value, store its coordinates
        coords = None
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    coords = (i, j)
                    break
            if coords is not None:  #break out of the loop if located (0)
                break

        limit = len(self.state) - 1  #boundary checking for puzzles row/col indexes

        #Define operators (moves)
        moves = {
            'down': (1, 0),   # Move blank down
            'up': (-1, 0),    # Move blank up
            'right': (0, 1),  # Move blank right
            'left': (0, -1)   # Move blank left
        }

        #Generate new states for each node's possible move
        for move, (coord_i, coord_j) in moves.items():
            new_i, new_j = coords[0] + coord_i, coords[1] + coord_j
            if 0 <= new_i <= limit and 0 <= new_j <= limit:  #Check new position's bounds
                #Check previous move to avoid reversing the last move to create potential cycles etc. 
                if not (self.move and move == {'down': 'up', 'up': 'down', 'left': 'right', 'right': 'left'}.get(self.move)):
                    #Create new state by copying the current state
                    new_state = [row[:] for row in self.state]
                    #Swap the blank with adjacent tile
                    new_state[coords[0]][coords[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[coords[0]][coords[1]]
                    
                    #Create new node instance for new state & add as child to parent node
                    new_node = Node(new_state, self.g + 1, move, self)
                    self.add_child(new_node)
