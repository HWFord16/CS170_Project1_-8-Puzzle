from node import Node
from tree import Tree

def graph_search(problem, misplaced_tiles = False, euclidean = False):
    start_time = time.time() #start measuring run time

    initial_state = problem[0]
    goal_state = problem[1]

    frontier = dict()
    explored = dict()
    num_nodes_expanded = 0
    max_frontier_size = 0

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
          total_runtime = time.time() - start_time
          return {"runtime": total_runtime, "numNodes": num_nodes_expanded, "frontierSize": max_frontier_size}
          #return frontier[t(pick_state)]

        # expand & remove from frontier while keeping tack of metrics
        frontier[t(pick_state)].expand()
        num_nodes_expanded += 1         #node count for time complexity
        max_frontier_size= max(max_frontier_size, len(frontier)) #frontier size for space complexity

        #pick the node in frontier run the chosen algorithm from func. param
        for child in frontier[t(pick_state)].children:
            child_state_t = t(child.state)
            if child_state_t not in explored and child_state_t not in frontier:
                if (misplaced_tiles): child.h = lambda x: child.misplaced_tiles()
                if (euclidean): child.h = lambda x: child.euclidean()

                frontier[child_state_t] = child

        # set current state to "explored" and remove from frontier
        explored[t(pick_state)] = True
        del frontier[t(pick_state)]

    #end search algo timer and return metrics for processing
    total_runTime= time.time() - start_time
    return {"runtime": total_runtime, "numNodes": num_nodes_expanded, "frontierSize": max_frontier_size}

def generate_reports(results):
    #Prep data for pandas DataFrame from results param
    data = {
        'Difficulty': [],
        'Algorithm': [],
        'Runtime': [],
        'Nodes Expanded': [],
        'Max Frontier Size': []
    }

    #Fill data dictionary from results list of dictionaries
    for result in results:
        difficulty, algorithm, metrics = result
        data['Difficulty'].append(difficulty)
        data['Algorithm'].append(algorithm)
        data['Runtime'].append(metrics['runtime'])
        data['Nodes Expanded'].append(metrics['numNodes'])
        data['Max Frontier Size'].append(metrics['frontierSize'])

    df = pd.DataFrame(data)
    df.sort_values('Difficulty', inplace=True)

    #Aggregate data of max values
    grouped_df = df.groupby(['Difficulty', 'Algorithm']).max().reset_index()

    # Pivot data to prepare for visualization
    runtime_df = grouped_df.pivot(index='Difficulty', columns='Algorithm', values='Runtime')
    nodes_expanded_df = grouped_df.pivot(index='Difficulty', columns='Algorithm', values='Nodes Expanded')
    max_frontier_size_df = grouped_df.pivot(index='Difficulty', columns='Algorithm', values='Max Frontier Size')

    #Helper Function to Plot function graph and creating table data
    def plot_metric_and_table(df, title, ylabel):
        fig, ax = plt.subplots(figsize=(12, 6))
        #Plot the bar graph
        df.plot(kind='bar', ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Puzzle Difficulty')
        ax.set_ylabel(ylabel)
        ax.legend(title="Algorithm")
        ax.grid(True, linestyle='--')

        #Add table at the bottom of the graph
        table_data = df.round(2).reset_index().values
        table_col_labels = ['Difficulty'] + list(df.columns)
        table_ax = fig.add_axes([0.1, -0.3, 0.8, 0.2], frame_on=False)
        table_ax.axis('off')
        table_ax.table(cellText=table_data, colLabels=table_col_labels, loc='center', cellLoc='center')

        plt.subplots_adjust(bottom=0.3)
        plt.show()

    #Call helper function to Generate separate graphs and tables for each metric
    plot_metric_and_table(runtime_df, 'Maximum Runtime by Puzzle Difficulty', 'Runtime (seconds)')
    print("\n\n")
    plot_metric_and_table(nodes_expanded_df, 'Maximum Number of Nodes Expanded by Puzzle Difficulty', 'Number of Nodes Expanded')
    print("\n\n")
    plot_metric_and_table(max_frontier_size_df, 'Maximum Frontier Size by Puzzle Difficulty', 'Max Frontier Size')

    
def main():
    print("Welcome to atole027's, spaka002's, and hwill006's 8 puzzle solver.\n")

    results = []  #list to hold results of algorithms on puzzles
    test_cases = {
        "Trivial": [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        "Very Easy": [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
        "Easy": [[1, 2, 0], [4, 5, 3], [7, 8, 6]],
        "Doable": [[0, 1, 2], [4, 5, 3], [7, 8, 6]],
        #"Oh Boy": [[8, 7, 1], [6, 0, 2], [5, 4, 3]] #takes too long
    }

    while True:
        #Initialize puzzle variables
        initial_state = []
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        problem = (initial_state, goal_state)

        #Prompt User Input for Puzzle
        choicePuzzle = input('Type "1" to use a default puzzle, "2" to enter your own puzzle, or "3" to run test cases: ')

        #input validation
        while choicePuzzle not in ('1', '2', '3'):
            choicePuzzle = input('Invalid Choice. Type "1" to use a default puzzle, "2" to enter your own puzzle, or "3" to run test cases: ')

        #Default Puzzle
        if choicePuzzle == "1":
          initial_state.append([1, 8, 2])
          initial_state.append([0, 4, 3])
          initial_state.append([7, 6, 5])

        #Custom Puzzle
        elif choicePuzzle == "2":
            print('Enter your puzzle, use a zero to represent the blank.')
            for i in range(3):
                row = input(f'Enter row {i+1}, use spaces between numbers: ')
                initial_state.append([int(num) for num in row.split()])

        #Prompt User for choice of algorithm
        if choicePuzzle in ('1', '2'):
            print('\nEnter your choice of algorithm:')
            print('1. Uniform Cost Search')
            print('2. A* with the Misplaced Tile heuristic')
            print('3. A* with the Euclidean distance heuristic')
            algorithmChoice = input()

            #call the correct algorithm off user choice
            if algorithmChoice in ('1', '2', '3'):
                print("\nGenerating Solution Path\n\n")
                if algorithmChoice == '1':
                    algo= "Uniform Search Cost"
                    result = graph_search(problem)
                elif algorithmChoice == '2':
                    algo = "A* Misplaced Tile"
                    result = graph_search(problem, misplaced_tiles=True)
                elif algorithmChoice == '3':
                    algo= "A* Euclidean"
                    result = graph_search(problem, euclidean=True)

                if(choicePuzzle == "1"):
                  results.append(("Default", algo , result))
                else: results.append(("Custom",algo, result))

        #Aumatically execute all test cases and use all three algorithms
        elif choicePuzzle == "3":
            for difficulty, puzzle in test_cases.items():
                print(f"\nTesting {difficulty} puzzle with all algorithms:")
                for alg_num, alg_name in  enumerate(["Uniform Cost Search", "A* Misplaced Tile", "A* Euclidean"], start=1):
                    print(f"Running {alg_name} on {difficulty} puzzle")
                    problem = (puzzle, goal_state)
                    result = graph_search(problem, misplaced_tiles=(alg_num==2), euclidean=(alg_num==3))
                    results.append((difficulty, alg_name, result))

        #Re-prompt user to for another round of puzzle solving
        cont = input('\nWould you like to solve another puzzle? (Y/N): ')
        if cont.upper() != 'Y':
            break

    if results:
        generate_reports(results)  # Call this outside the loop, once all data is collected
        print("Results processing complete.")

if __name__ == '__main__':
    main()