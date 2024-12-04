# định nghĩa graph và  thuật toán bfs cho xác ướp
from collections import deque

class Graph:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.numVertiecs = numRows * numCols
        self.adjList = [[] for _ in range(self.numVertiecs)]

    def __str__(self):
        return self.adjList

    def addEdge(self, v1, v2):
        if v2 not in self.adjList[v1]:
            self.adjList[v1].append(v2)

        if v1 not in self.adjList[v2]:
            self.adjList[v2].append(v1)

    def addRectangleEdges(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                current = row * self.numCols + col
                # Kiểm tra và thêm cạnh tới đỉnh ở bên phải
                if col < self.numCols - 1:
                    self.addEdge(current, current + 1)
                # Kiểm tra và thêm cạnh tới đỉnh ở bên dưới
                if row < self.numRows - 1:
                    self.addEdge(current, current + self.numCols)



    def findListPath(self, start, end):

        queue = deque([[start]])
        visited = set([start])
        minLength = None

        resultPaths = [] 


        while queue:
            path = queue.popleft()
            current = path[-1]

            # dừng khi tất cả các đường đi đã dài hơn đường ngắn nhất
            if minLength is not None and len(path) > minLength:
                break

            for neighbour in self.adjList[current]:
                if neighbour in visited and (minLength is not None and len(path) > minLength):
                    continue

                newPath = list(path)
                newPath.append(neighbour)

                if neighbour == end:
                    resultPaths.append(newPath[1]) # for game
                    # resultPaths.append(newPath)
                    minLength = len(newPath)
                else:
                    queue.append(newPath)
                    visited.add(neighbour)


        return resultPaths # [ [0,2,4,5], [0,2,3,6], .... ]

# graph = Graph(6,6)
# graph.addRectangleEdges()
# print(graph.adjList)
# listPath = graph.findListPath(9,1)

# print(listPath)