class Tree:
    def __init__(self, root):
        self.root = root  #root node

    def trace_path(self, goal_node):
        #fetch from Goal node --> root node for solution path
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()  #reverse path from root to goal for return
        return path

    def output_solution(self, goal_node):
        #display the solution from the trace
        path = self.trace_path(goal_node)
        for node in path:
            print("Step {}: ".format(node.g))
            for row in node.state:  # Iterate and output each row vector in matrix
              print(' '.join(map(str, row))) #convert each element to str and format
            if node.move:
                print("Move: ", node.move)
            print()

    def add_node(self, parent_node, child_node):
        parent_node.add_child(child_node)
