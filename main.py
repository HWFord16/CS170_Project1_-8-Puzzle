from node import Node
from tree import Tree

def graph_search(problem, misplaced_tiles = False, euclidean = False):

    initial_state = problem[0]
    goal_state = problem[1]

    frontier = dict()
    explored = dict()

    # little function to convert lists of lists to tuples of tuples for hashing
    def t(x): return tuple(tuple(y) for y in x)

    # initialize root node in tree for frontier
    initial_node = Node(initial_state, depth=0, goal_state = goal_state)
    tree = Tree(initial_node)
    frontier[t(initial_state)] = initial_node

    # Set heuristic function based on parameter flags
    # else default H(n)=0  --> Uni. cost search (UCS)
    if (misplaced_tiles):
      frontier[t(initial_state)].h = lambda x: frontier[t(initial_state)].misplaced_tiles()
    if (euclidean):
      frontier[t(initial_state)].h = lambda x: frontier[t(initial_state)].euclidean()

    # execute loop while frontier is not empty
    while(frontier):
        # pick from frontier using minimum heuristic function cost
        min_cost = min(frontier[x].heuristic() for x in frontier)
        pick_state = next(state for state in frontier if frontier[state].heuristic() == min_cost and state not in explored)

        # test if goal state
        if (t(pick_state) == t(goal_state)):
          tree.output_solution(frontier[t(pick_state)]) #trace solution path from goal node to root
          return frontier[t(pick_state)]

        # expand & remove from frontier
        frontier[t(pick_state)].expand()

        for child in frontier[t(pick_state)].children:
            child_state_t = t(child.state)
            if child_state_t not in explored and child_state_t not in frontier:

                if (misplaced_tiles): child.h = lambda x: child.misplaced_tiles()
                if (euclidean): child.h = lambda x: child.euclidean()

                # child.h = lambda x: child.misplaced_tiles()  # Set the heuristic function for each child
                frontier[child_state_t] = child

        # set current state to "explored" and remove from frontier
        explored[t(pick_state)] = True
        del frontier[t(pick_state)]

    return False

def main():
    print("Welcome to atole027's, spaka002's, and hwill006's 8 puzzle solver.\n")
    
    test_cases = {
        "Trivial": [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        "Very Easy": [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
        "Easy": [[1, 2, 0], [4, 5, 3], [7, 8, 6]],
        "Doable": [[0, 1, 2], [4, 5, 3], [7, 8, 6]],
        #"Oh Boy": [[8, 7, 1], [6, 0, 2], [5, 4, 3]] #takes too long
    }

    while True:
        # Initialize puzzle variables
        initial_state = []
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        problem = (initial_state, goal_state)

        #Prompt User Input for Puzzle
        choicePuzzle = input('Type "1" to use a default puzzle, "2" to enter your own puzzle, or "3" to run test cases: ')

        while choicePuzzle not in ('1','2','3'):
          choicePuzzle = input('Invalid Choice. Type "1" to use a default puzzle, "2" to enter your own puzzle, or "3" to run test cases: ')
        
        if choicePuzzle == "1":
          initial_state.append([1, 8, 2])
          initial_state.append([0, 4, 3])
          initial_state.append([7, 6, 5])

        elif choicePuzzle == "2":
            print('Enter your puzzle, use a zero to represent the blank.')
            for i in range(3):
                row = input('Enter row ' + str(i+1) + ', use spaces between numbers: ')
                initial_state.append([int(num) for num in row.split()])
        elif choicePuzzle == "3":
          #Automatically execute all test cases for all three algorithms
          for difficulty, puzzle in test_cases.items():
              print(f"\nTesting {difficulty} puzzle with all algorithms:")
              for alg_num, alg_name in enumerate(["Uniform Cost Search", "A* Misplaced Tile", "A* Euclidean"], start=1):
                  print(f"Running {alg_name} on {difficulty} puzzle\n")
                  if alg_num == 1:
                      final_node = graph_search((puzzle, goal_state))
                  elif alg_num == 2:
                      final_node = graph_search((puzzle, goal_state), misplaced_tiles=True)
                  elif alg_num == 3:
                      final_node = graph_search((puzzle, goal_state), euclidean=True)

        while (choicePuzzle == '1' or choicePuzzle == '2'):
            #Prompt User Input for Algorithm Choice
            print('\nEnter your choice of algorithm:')
            print('1. Uniform Cost Search')
            print('2. A* with the Misplaced Tile heuristic')
            print('3. A* with the Euclidean distance heuristic')
            algorithmChoice = input()

            if algorithmChoice == '1':
                print("\n Generating Solution Steps\n\n")
                final_node = graph_search(problem)
                break
            elif algorithmChoice == '2':
                print("\n Generating Solution Steps\n\n")
                final_node = graph_search(problem, misplaced_tiles=True)
                break
            elif algorithmChoice == '3':
                print("\n Generating Solution Steps\n\n")
                final_node = graph_search(problem, euclidean=True)
                break
            else:
                print('\nInvalid. Select an algorithm by entering a number 1-3:')
                algorithmChoice = input()

        #Check if the user wants to continue or exit
        cont = input('\nWould you like to solve another puzzle? (Y/N): ')
        if cont.upper() != 'Y':
            print("\n\nThanks for Playing!\n\n")
            break

if __name__ == '__main__':
    main()