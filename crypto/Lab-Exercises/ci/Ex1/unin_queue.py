from queue import Queue

class Graph:
    def __init__(self):
        self.graph = {}
    
    def add_node(self, n):
        if n not in self.graph:
            self.graph[n] = []
            print(f"Node '{n}' added.")
        else:
            print(f"Node '{n}' already exists.")
    
    def add_edge(self, a, b):
        if a not in self.graph:
            print(f"Node '{a}' not found. Add it first.")
            return
        if b not in self.graph:
            print(f"Node '{b}' not found. Add it first.")
            return
        
        # Add edge in both directions for undirected graph
        if b not in self.graph[a]:
            self.graph[a].append(b)
        if a not in self.graph[b]:
            self.graph[b].append(a)
        
        print(f"Edge added: {a} <-> {b}")
    
    def display_graph(self):
        print("\nGraph (Adjacency List):")
        for n, neighbors in self.graph.items():
            print(f"{n}: {neighbors}")
    
    def bfs(self, start, goal):
        if start not in self.graph:
            print(f"Start node '{start}' not in graph.")
            return
        if goal not in self.graph:
            print(f"Goal node '{goal}' not in graph.")
            return
        
        seen = set()
        fringe = Queue()
        fringe.put(start)
        prev = {start: None}
        
        print(f"\nBFS Search from '{start}' to '{goal}':")
        print(f"Initial fringe: [{start}]\n")
        
        while not fringe.empty():
            # Get current fringe contents for display
            temp = list(fringe.queue)
            print(f"Fringe: {temp}")
            
            node = fringe.get()
            print(f"Visiting: {node}")
            
            if node == goal:
                print(f"\nGoal '{goal}' found!")
                self.print_path(prev, start, goal)
                return
            
            if node in seen:
                continue
            
            seen.add(node)
            
            for child in self.graph[node]:
                if child not in seen:
                    if child not in prev:
                        prev[child] = node
                        fringe.put(child)
            
            print(f"Visited: {seen}\n")
        
        print(f"Goal '{goal}' not reachable from '{start}'.")
    
    def print_path(self, prev, start, goal):
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        print(f"Path: {' -> '.join(path)}")


def main():
    g = Graph()
    
    print("=== Uninformed Search (BFS) - Queue Implementation ===\n")
    
    # Get number of nodes
    n = int(input("Enter number of nodes: "))
    
    print("\nEnter node names:")
    for i in range(n):
        name = input(f"Node {i+1}: ")
        g.add_node(name)
    
    # Menu for operations
    while True:
        print("\n--- Menu ---")
        print("1. Add Node")
        print("2. Add Edge")
        print("3. Display Graph")
        print("4. Run BFS")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            name = input("Enter node name: ")
            g.add_node(name)
        
        elif choice == '2':
            a = input("Enter source node: ")
            b = input("Enter destination node: ")
            g.add_edge(a, b)
        
        elif choice == '3':
            g.display_graph()
        
        elif choice == '4':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            g.bfs(start, goal)
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
