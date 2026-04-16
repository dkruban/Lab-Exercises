from queue import Queue
def addnode(graph,node):
    if node not in graph:
        graph[node] = []

def addedge(graph,x,y):
    if y not in graph[x]:
        graph[x].append(y)
    if x not in graph[y]:
        graph[y].append(x)

def deletenote(graph,node):
   if node in graph:
      del graph[node]
      for i in graph.values():
         if node in i:
            i.remove(node)
   else:
      print("\n Node does not exists in the graph ")

def deleteedge(graph,x,y):
   if x in graph and y in graph[x]:
      graph[x].remove(y)
   if y in graph and x in graph[y]:
      graph[y].remove(x)

def bfs(graph,start,goal):
    visited = set([start])
    q = Queue()
    q.put(start)
    result = []
    while not q.empty():
        print("Fringe queue :",list(q.queue))
        currentnode  = q.get()
        result.append(currentnode)
        print("visited : ",result)
        if currentnode in goal:
            print("Goal found \n path : ",result)
            break
        for i in graph.get(currentnode,[]):
           if i not in visited:
              q.put(i)
              visited.add(i)

def display(graph):
    print("Adjacency list ")
    for i in graph:
        print(i,graph[i])

graph = {}
n = int(input("Enter no of nodes : "))
print("Enter nodes : ")
for i in range(n):
    node = input()
    addnode(graph,node)
e = int(input("Enter no of edges : "))
print("Enter edges : ")
for i in range(e):
    x,y = input().split()
    addedge(graph,x,y)
display(graph)
while(true):
   print(" Enter :- \n\t1 to add node\n\t2 to add edge\n\t3 to delete node\n\t4 to delete edge\n\t 5 to bfs\n\t 6 to exit")
   ch = int(input("Enter your choice : "))
   if(ch == 1):
      print("Enter node : ")
      node = input()
      addnode(graph,node)
   elif(ch == 2):
      print("Enter edge x y : ")
      x,y = input().split()
      addedge(graph,x,y)
   elif(ch == 3):
      print("Enter node to deletenode : ")
      deletenode(graph,node)
   elif(ch == 4):
      print("Enter the x y edge to delete")
      x,y=input().split()
      deleteedge(graph,x,y)
   elif(ch == 5):
      s=input("Enter start node : ")
      g=input("Enter goal node : ")
      bfs(graph,s,g)
   elif(ch == 6):
      break
   else:
      print("Invalid choice")
