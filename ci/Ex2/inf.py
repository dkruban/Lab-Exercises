from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.cost_matrix = {}
        self.heuristics = {}
    
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
        
        if node2 not in self.adj_list[node1]:
            self.adj_list[node1].append(node2)
        if node1 not in self.adj_list[node2]:
            self.adj_list[node2].append(node1)
        
        if node1 not in self.cost_matrix:
            self.cost_matrix[node1] = {}
        if node2 not in self.cost_matrix:
            self.cost_matrix[node2] = {}
        
        self.cost_matrix[node1][node2] = cost
        self.cost_matrix[node2][node1] = cost
        
        print(f"Edge added: {node1} <-> {node2} (cost: {cost})")
    def del_node(self, node):
        if node not in self.adj_list:
            print("Node not present!")
            return
        del(self.adj_list[node])
        for i,l in self.adj_list.items():
            if node in l:
                l.remove(node)

    def del_edge(self, node1, node2):
        if node1 not in self.adj_list or node2 not in self.adj_list:
            print("Invalid edge!")
            return
        self.adj_list[node1].remove(node2)
        self.adj_list[node2].remove(node1)

    def display_graph(self):
        print("\nGraph (Adjacency List):")
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {neighbors}")            

    def ucs(self, start, goal):
        if start not in self.adj_list:
            print(f"Start node '{start}' not in graph.")
            return
        if goal not in self.adj_list:
            print(f"Goal node '{goal}' not in graph.")
            return
        

        explored = set()
        fringe = []  # List of (cost, node, parent)
        parent = {}
        g_score = {}
        f_score = {}

        for node in self.adj_list:
            g_score[node] = float('inf')
            f_score[node] = float('inf')
        g_score[start] = 0
        f_score[start] = self.heuristics[start]
        
        fringe.append((f_score[start], start))
        print(f"\n Search from '{start}' to '{goal}':")
        print(f"Initial fringe: [({start}, f(n)=0+{self.heuristics[start]}={self.heuristics[start]}]\n")
        
        while fringe:
            print(f"Fringe: {fringe}")
            
            fringe.sort(key=lambda x: x[0])
            current_f, current = fringe.pop(0)
            
            print(f"Visiting: {current} (f(n)={current_cost+self.heuristics[current]})")
            
            if current == goal:
                parent[current] = current_parent
                print(f"\nGoal '{goal}' found with cost {current_cost}!")
                self.print_path_with_cost(parent, start, goal, current_cost)
                return
            
            for neighbor in self.adj_list[current]:
                edge_cost = self.cost_matrix[current][neighbor]
                tent_g_score = g_score[current] + edge_cost
                if tent_g_score < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = tent_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristics[neighbor]
                    in_fringe = False
                    for f, node in fringe:
                        if node==neighbor:
                            in_fringe = True
                            break
                if not in_fringe:
                    fringe.append((f_score[neighbor], neighbor))  
            
            
            explored.add(current)
            parent[current] = current_parent
            
            for neighbor in self.adj_list[current]:
                if neighbor not in explored:
                    edge_cost = self.cost_matrix.get(current, {}).get(neighbor, 1)
                    child_cost = current_cost + edge_cost
                    in_fringe = False
                    for i, (cost, node, par) in enumerate(fringe):
                        if node == neighbor:
                            in_fringe = True
                            if child_cost < cost:
                                fringe[i] = (child_cost, neighbor, current)
                                print(f"  Updated {neighbor} in fringe (new cost={child_cost})")
                            break
                    
                    if not in_fringe:
                        fringe.append((child_cost, neighbor, current))
                        print(f"  Added {neighbor} to fringe (cost={child_cost})")
            
            print(f"Explored: {explored}\n")
        
        print(f"Goal '{goal}' not reachable from '{start}'.")
    
    def print_path_with_cost(self, parent, start, goal, total_cost):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        print(f"Path: {' -> '.join(path)}")
        print(f"Total Cost: {total_cost}")

    def print_path(self, parent, start, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        print(f"Path: {' -> '.join(path)}")
        print(f"Total cost: {len(path)-1}")



def main():
    graph = Graph()

    print("Uninformed Search algos\n")
    num_nodes = int(input("Enter number of nodes: "))

    print("\nEnter node names:")
    for i in range(num_nodes):
        node = input(f"Node {i+1}: ")
        graph.add_node(node)

    while True:
        print("Menu")
        print("1. Add Node")
        print("2. Add Edge")
        print("3. Delete node")
        print("4. Delete edge")
        print("5. Display Graph")
        print("6. Run BFS")
        print("7. Run DFS")
        print("8. Run UCS")
        print("9. Exit")
        
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
            node = input("Enter node name: ")
            graph.del_node(node)

        elif choice == '4':
            node1 = input("Enter source node: ")
            node2 = input("Enter destination node: ")
            graph.del_edge(node1, node2)

        elif choice == '5':
            graph.display_graph()
        
        elif choice == '6':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.bfs(start, goal)
        
        elif choice == '7':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.dfs(start,goal)

        elif choice == '8':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.ucs(start, goal)
            
        elif choice == '9':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

