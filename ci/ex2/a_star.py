class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []
            print(f"Node {node} added")
        else:
            print("Node already exists")

    def delete_node(self, node):
        if node in self.adj:
            for i in self.adj:
                self.adj[i] = [x for x in self.adj[i] if x[0] != node]
            del self.adj[node]
            print(f"Node {node} deleted")
        else:
            print("Node not found")

    def add_edge(self, n1, n2, cost):
        if n1 in self.adj and n2 in self.adj:
            self.delete_edge(n1, n2)
            self.adj[n1].append((n2, cost))
            self.adj[n2].append((n1, cost))
            print(f"Edge {n1}-{n2} added with cost {cost}")
        else:
            print("Both nodes must exist")

    def delete_edge(self, n1, n2):
        if n1 in self.adj and n2 in self.adj:
            self.adj[n1] = [x for x in self.adj[n1] if x[0] != n2]
            self.adj[n2] = [x for x in self.adj[n2] if x[0] != n1]
        else:
            print("Nodes not found")

    def display(self):
        print("\nAdjacency List:")
        for i in self.adj:
            print(f"{i} -> {self.adj[i]}")

def a_star(graph, start, goal):
    if start not in graph.adj or goal not in graph.adj:
        print("Start or Goal node not found")
        return None

    print(f"\nEnter heuristic values (h) for reaching {goal}:")
    heuristics = {node: int(input(f"  h({node}): ")) for node in graph.adj}
    queue = [[heuristics[start], 0, start, [start]]]
    closed_list = []
    step = 1

    print("\n--- A* Search Traversal Steps ---")
    while queue:

        queue.sort(key=lambda x: x[0])
        open_list_display = [item[2] for item in queue]
        print(f"\nStep {step}")
        print(f"OPEN: {open_list_display}")
        print(f"CLOSED: {closed_list}")

        f_cost, g_cost, current, path = queue.pop(0)
        print(f"Selected: {current} g: {g_cost} h: {heuristics[current]} f: {f_cost}")

        if current == goal:
            print("Goal node found!")
            print(f"Final Path: {' -> '.join(path)}")
            print(f"Total Cost: {g_cost}")
            return path, g_cost

        if current not in closed_list:
            closed_list.append(current)

        for neighbor, weight in graph.adj[current]:
            if neighbor in closed_list:
                continue

            new_g = g_cost + weight
            new_f = new_g + heuristics[neighbor]


            found_in_queue = False
            for i in range(len(queue)):
                if queue[i][2] == neighbor:
                    found_in_queue = True
                    if new_g < queue[i][1]:
                        queue[i] = [new_f, new_g, neighbor, path + [neighbor]]
                    break

            if not found_in_queue:
                queue.append([new_f, new_g, neighbor, path + [neighbor]])

        step += 1

    print("Goal not found")
    return None
graph = Graph()
try:
    n_nodes = int(input("Enter number of nodes: "))
    for _ in range(n_nodes):
        graph.add_node(input("Enter node: "))

    n_edges = int(input("Enter number of edges: "))
    for _ in range(n_edges):
        u = input("Enter node 1: ")
        v = input("Enter node 2: ")
        c = int(input("Enter cost: "))
        graph.add_edge(u, v, c)
except ValueError:
    print("Invalid input, please enter numeric values for counts/costs.")
while True:
    print("\n--- MENU ---")
    print("1. Add Node     \n 2. Delete Node")
    print("3. Add Edge      \n4. Delete Edge")
    print("5. Display       \n6. A* Search")
    print("7. Exit")

    choice = input("Enter choice: ")
    if choice == '1':
        graph.add_node(input("Enter node: "))
    elif choice == '2':
        graph.delete_node(input("Enter node to delete: "))
    elif choice == '3':
        u, v, c = input("Node 1: "), input("Node 2: "), int(input("Cost: "))
        graph.add_edge(u, v, c)
    elif choice == '4':
        graph.delete_edge(input("Node 1: "), input("Node 2: "))
    elif choice == '5':
        graph.display()
    elif choice == '6':
        a_star(graph, input("Start Node: "), input("Goal Node: "))
    elif choice == '7':
        print("Exiting...")
        break
    else:
        print("Invalid choice")
