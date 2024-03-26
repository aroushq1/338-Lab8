""" 
    The Depth-First Search algorithm is used to implement topological sorting.
    It is used because it can efficiently explore all edges and vertices of a given graph in order to find the complete
    dependency structure among vertices (nodes).
"""
#ai was used to generate this code
class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors = set()

    def addNeighbor(self, neighbor):
        self.neighbors.add(neighbor)

    def getNeighbors(self):
        return self.neighbors

class Graph:
    def __init__(self):
        self.vertices = {}  # Dictionary to store nodes

    def addNode(self, data):
        if data not in self.vertices:
            self.vertices[data] = Node(data)
        return self.vertices[data]

    def addEdge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].addNeighbor(v2)
        else:
            if v1 not in self.vertices:
                self.addNode(v1)
            if v2 not in self.vertices:
                self.addNode(v2)
            self.vertices[v1].addNeighbor(v2)

    def isdag(self):
        def dfs_visit(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.vertices[node].getNeighbors():
                if neighbor not in visited:
                    if dfs_visit(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False
        
        visited = set()
        rec_stack = set()
        for node in self.vertices:
            if node not in visited:
                if dfs_visit(node, visited, rec_stack):
                    return False  # Cycle found
        return True  # No cycle found, it's a DAG

    def toposort(self):
        if not self.isdag():
            print("Graph is not a DAG.")
            return None  # Return None if not a DAG
        
        def dfs_visit(node, visited, stack):
            visited.add(node)
            for neighbor in self.vertices[node].getNeighbors():
                if neighbor not in visited:
                    dfs_visit(neighbor, visited, stack)
            stack.append(node)
        
        visited = set()
        stack = []
        for node in self.vertices:
            if node not in visited:
                dfs_visit(node, visited, stack)
        
        return stack[::-1]  # Return the reversed stack for correct order

# Example usage
graph = Graph()
graph.addNode("A")
graph.addNode("B")
graph.addNode("C")
graph.addEdge("A", "B")
graph.addEdge("B", "C")

# Check if the graph is a DAG and print topological order if it is
if graph.isdag():
    print("Graph is a DAG.")
    print("Topological order:", [node for node in graph.toposort()])
else:
    print("Graph is not a DAG.")
