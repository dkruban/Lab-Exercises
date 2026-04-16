from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
            print(f"Node {node} added.")
            return True
        print(f"Node {node} already exists.")
        return False

    def add_edge(self, u, v):
        if u in self.adj_list and v in self.adj_list:
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
                self.adj_list[v].append(u)
                print(f"Edge added between {u} and {v}.")
                return True
        print(f"Error: One or both nodes '{u}', '{v}' do not exist.")
        return False

    def delete_edge(self, u, v):
        if u in self.adj_list and v in self.adj_list:
            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)
                self.adj_list[v].remove(u)
                print(f"Edge between {u} and {v} deleted.")
                return True
        print("Edge does not exist.")
        return False

    def delete_node(self, node):
        if node in self.adj_list:
            for neighbor in self.adj_list[node]:
                self.adj_list[neighbor].remove(node)
            del self.adj_list[node]
            print(f"Node '{node}' and all its connections deleted.")
            return True
        print(f"Node '{node}' not found.")
        return False

    def display_graph(self):
        print("\n--- Current Graph Structure (2026) ---")
        if not self.adj_list:
            print("The graph is empty.")
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {', '.join(map(str, neighbors)) if neighbors else 'No neighbors'}")

    def bfs_traversal_output(self, start, end):
        """Modified for 2026: Stops at 'end' and provides step-by-step output."""
        if start not in self.adj_list:
            return f"Error: Start node '{start}' not found."

        queue = deque([start])
        visited_order = []
        visited_set = {start}
        step = 1

        print(f"\n--- Starting BFS Traversal from '{start}' to '{end}' ---")

        while queue:
            
            print(f"Step {step}:")
            print(f"  Queue: {list(queue)}")
            print(f"  Visited Set: {sorted(list(visited_set))}")

            current = queue.popleft()
            visited_order.append(current)
            print(f"  Processing Node: {current}")

            
            if current == end:
                print(f"  Target node '{end}' reached! Terminating search.")
                break

            
            for neighbor in sorted(self.adj_list[current]):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    queue.append(neighbor)

            step += 1

        
        if end not in visited_order:
            print(f"\nNote: Traversal completed, but end node '{end}' was not reachable.")

        return "{" + ", ".join(map(str, visited_order)) + "}"


g = Graph()

print("\n--- Graph Manager Menu (2026) ---")
print("\n\t1. Add Node           \n\t2. Add Edge")
print("\n\t3. Delete Node         \n\t4. Delete Edge")
print("\n\t5. Display Full Graph  \n\t6. Run BFS Traversal (Stop at End Node)")
print("\n\t7. Exit")
while True:
    choice = input("Select an option: ")

    if choice == '1':
        node = input("Enter node name: ")
        g.add_node(node)
    elif choice == '2':
        try:
            nodes = input("Enter two nodes (space separated): ").split()
            g.add_edge(nodes[0], nodes[1])
        except (ValueError, IndexError):
            print("Input Error: Enter two names.")
    elif choice == '3':
        node = input("Enter node to delete: ")
        g.delete_node(node)
    elif choice == '4':
        try:
            nodes = input("Enter edge to delete (node1 node2): ").split()
            g.delete_edge(nodes[0], nodes[1])
        except (ValueError, IndexError):
            print("Input Error: Enter two names.")
    elif choice == '5':
        g.display_graph()
    elif choice == '6':
        start_node = input("Enter start node: ")
        end_node = input("Enter end node to stop at: ")
        result = g.bfs_traversal_output(start_node, end_node)
        print(f"\nFinal Traversal Sequence: {result}")
    elif choice == '7':
        print("Program closed.")
        break
    else:
        print("Invalid selection. Please choose 1-7.")
