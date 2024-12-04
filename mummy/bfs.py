from collections import deque 

# 1:[2,3]
class Graph:
    def __init__(self):
        self.graph = { }

    def addVertex(self, vertex1, vertex2):

        if vertex1 in self.graph:
            self.graph[vertex1].append(vertex2)
        else:
            self.graph[vertex1] = [vertex2]

        # dùng cho đồ thị vô hướng
        if vertex2 in self.graph:
            self.graph[vertex2].append(vertex1)
        else:
            self.graph[vertex2] = [vertex1]

    def bfs(self,start):
        visited = set()
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                print(vertex)

                for nei in self.graph[vertex]:
                    if nei not in visited:
                        queue.append(nei)

graph = Graph()

graph.addVertex(1,2)
graph.addVertex(1,3)
graph.addVertex(2,3)
graph.addVertex(2,4)
graph.addVertex(3,5)
graph.addVertex(4,5)
graph.addVertex(5,6)
graph.addVertex(6,7)
graph.addVertex(7,8)
graph.addVertex(7,9)

graph.bfs(1)