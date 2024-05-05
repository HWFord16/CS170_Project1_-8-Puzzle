class Node:
    def __init__(self, state, depth, move = None, parent = None, goal_state = None):
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
        if self.goal_state is None:  # Check if goal_state is defined
            return float('inf')

        count = 0    # Number or tiles out of place
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] != self.goal_state[i][j]:
                    count += 1
        return count

    def euclidean(self):
        if self.goal_state is None:  # Check if goal_state is defined
            return float('inf')

        goal_dict = dict()
        for i in range(3):
          for j in range(3):
            goal_dict[(i*3)+j+1] = (i, j)

        del goal_dict[(i*3)+j+1]

        D = lambda x, y, p: sum( [ (abs(x[i]-y[i]) ** p) for i in range(len(x))] ) ** (1/p)

        cost = 0    # total cost
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                cell = self.state[i][j]
                if (cell != 0): cost+= D((i, j), goal_dict[cell], 2)

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

            self.add_child(Node(new_state, depth=self.g+1, move="down", parent = self, goal_state = self.goal_state))
            del new_state

        if ((self.move != "down") and (coords[0] < limit)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]+1][coords[1]])
            new_state[coords[0]+1][coords[1]] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="up", parent = self, goal_state = self.goal_state))
            del new_state

        if ((self.move != "left") and (coords[1] > 0)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]][coords[1]-1])
            new_state[coords[0]][coords[1]-1] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="right", parent = self, goal_state = self.goal_state))
            del new_state

        if ((self.move != "right") and (coords[1] < limit)):
            new_state = [x.copy() for x in self.state.copy()].copy()
            new_state[coords[0]][coords[1]] = int(new_state[coords[0]][coords[1]+1])
            new_state[coords[0]][coords[1]+1] = 0

            self.add_child(Node(new_state, depth=self.g+1, move="left", parent = self, goal_state = self.goal_state))
            del new_state