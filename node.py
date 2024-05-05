import numpy as np
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

        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if (self.state[i][j] == 0):
                    coords = (i, j)

        limit = len(self.state)-1

        # just hardcoded all (4) of the moves possible for this state
        if ((self.move != "up") and (coords[0] > 0)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]-1][coords[1]])
            new_state[coords[0]-1][coords[1]] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="up", parent = self))
            del new_state

        if ((self.move != "down") and (coords[0] < limit)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]+1][coords[1]])
            new_state[coords[0]+1][coords[1]] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="down", parent = self))
            del new_state

        if ((self.move != "left") and (coords[1] > 0)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]][coords[1]-1])
            new_state[coords[0]][coords[1]-1] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="left", parent = self))
            del new_state

        if ((self.move != "right") and (coords[1] < limit)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]][coords[1]+1])
            new_state[coords[0]][coords[1]+1] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="right", parent = self))
            del new_state