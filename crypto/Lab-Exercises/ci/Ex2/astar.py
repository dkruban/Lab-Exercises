from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.cost_matrix = {}  # cost_matrix[(node1, node2)] = cost
        self.heuristics = {}   # heuristics[node] = h(n) value
    
    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
            print(f"Node '{node}' added.")
        else:
            print(f"Node '{node}' already exists.")
    
    def add_edge(self, node1, node2, cost=1):
        if node1 not in self.adj_list:
            print(f"Node '{node1}' not found. Add it first.")
            return
        if node2 not in self.adj_list:
            print(f"Node '{node2}' not found. Add it first.")
            return
        
        # Add edge in both directions for undirected graph
        if node2 not in self.adj_list[node1]:
            self.adj_list[node1].append(node2)
        if node1 not in self.adj_list[node2]:
            self.adj_list[node2].append(node1)
        
        # Store costs in matrix (nested dict)
        if node1 not in self.cost_matrix:
            self.cost_matrix[node1] = {}
        if node2 not in self.cost_matrix:
            self.cost_matrix[node2] = {}
        
        self.cost_matrix[node1][node2] = cost
        self.cost_matrix[node2][node1] = cost
        
        print(f"Edge added: {node1} <-> {node2} (cost: {cost})")

    def display_graph(self):
        print("\nGraph (Adjacency List):")
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {neighbors}")
    
    def set_heuristic(self, node, h_value):
        if node not in self.adj_list:
            print(f"Node '{node}' not in graph.")
            return
        self.heuristics[node] = h_value
        print(f"Heuristic for '{node}' set to {h_value}")
    
    def astar(self, start, goal):
        """
        A* Search implementation
        f(n) = g(n) + h(n)
        g(n) = actual cost from start to n
        h(n) = heuristic estimate from n to goal
        """
        if start not in self.adj_list:
            print(f"Start node '{start}' not in graph.")
            return
        if goal not in self.adj_list:
            print(f"Goal node '{goal}' not in graph.")
            return
        
        # Check if heuristics are set for all nodes
        for node in self.adj_list:
            if node not in self.heuristics:
                print(f"Heuristic not set for node '{node}'. Please set heuristics first.")
                return
        
        # Initialize
        fringe = []  # List of (f_score, node)
        parent = {}
        
        # Initialize g_score and f_score for all nodes
        g_score = {}
        f_score = {}
        for node in self.adj_list:
            g_score[node] = float('inf')
            f_score[node] = float('inf')
        
        g_score[start] = 0
        f_score[start] = self.heuristics[start]
        
        fringe.append((f_score[start], start))
        
        print(f"\nA* Search from '{start}' to '{goal}':")
        print(f"Initial fringe: [({start}, g=0, h={self.heuristics[start]}, f={f_score[start]})]\n")
        
        while fringe:
            # Display current fringe
            print("Fringe: [", end="")
            for i, (f, node) in enumerate(fringe):
                if i > 0:
                    print(", ", end="")
                print(f"({node}, g={g_score[node]}, h={self.heuristics[node]}, f={f_score[node]})", end="")
            print("]")
            
            # Sort by f_score and pop node with lowest f_score
            fringe.sort()
            current_f, current = fringe.pop(0)
            
            print(f"Visiting: {current} (g={g_score[current]}, h={self.heuristics[current]}, f={f_score[current]})")
            
            # GOAL TEST
            if current == goal:
                print(f"\nGoal '{goal}' found!")
                self.reconstruct_path(parent, start, goal, g_score[current])
                return
            
            # Expand node - check each neighbor
            for neighbor in self.adj_list[current]:
                # Calculate tentative g_score
                edge_cost = self.cost_matrix[current][neighbor]
                tentative_g_score = g_score[current] + edge_cost
                
                # If this path to neighbor is better than any previous one
                if tentative_g_score < g_score[neighbor]:
                    # This path is the best so far, record it
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristics[neighbor]
                    
                    # Check if neighbor is already in fringe
                    in_fringe = False
                    for f, node in fringe:
                        if node == neighbor:
                            in_fringe = True
                            break
                    
                    if not in_fringe:
                        fringe.append((f_score[neighbor], neighbor))
                        print(f"  Added {neighbor} to fringe (g={g_score[neighbor]}, h={self.heuristics[neighbor]}, f={f_score[neighbor]})")
                    else:
                        print(f"  Updated {neighbor} in fringe (g={g_score[neighbor]}, h={self.heuristics[neighbor]}, f={f_score[neighbor]})")
            
            print()
        
        print(f"Goal '{goal}' not reachable from '{start}'.")
    
    def reconstruct_path(self, came_from, start, goal, total_cost):
        """Reconstruct path from came_from dictionary"""
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        print(f"Path: {' -> '.join(path)}")
        print(f"Total Cost: {total_cost}")


def main():
    graph = Graph()

    print("=== A* Search ===\n")

    # Get number of nodes
    num_nodes = int(input("Enter number of nodes: "))

    print("\nEnter node names:")
    for i in range(num_nodes):
        node = input(f"Node {i+1}: ")
        graph.add_node(node)

    # Menu for operations
    while True:
        print("\n--- Menu ---")
        print("1. Add Node")
        print("2. Add Edge")
        print("3. Display Graph")
        print("4. Set Heuristic for Node")
        print("5. Run A* Search")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            node = input("Enter node name: ")
            graph.add_node(node)
        
        elif choice == '2':
            node1 = input("Enter source node: ")
            node2 = input("Enter destination node: ")
            cost = int(input("Enter edge cost: "))
            graph.add_edge(node1, node2, cost)
        
        elif choice == '3':
            graph.display_graph()
        
        elif choice == '4':
            node = input("Enter node name: ")
            h_value = float(input(f"Enter heuristic value (SLD) for '{node}': "))
            graph.set_heuristic(node, h_value)
        
        elif choice == '5':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.astar(start, goal)
            
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
