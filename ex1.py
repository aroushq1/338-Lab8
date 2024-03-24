class Graph:
    def __init__(self):
        self.vertices = {}  # Dictionary to store nodes
        self.connections = {}  # Dictionary to store edges

    def addNode(self, data):
        # Creates a new graph node internally storing the string passed as a parameter. Returns a Node object
        self.vertices[data] = Node(data)
        return self.vertices[data]

    def removeNode(self, node): 
        # Removes the node
        if node in self.vertices:
            del self.vertices[node]
            # Remove edges associated with this vertex
            for connection in list(self.connections.keys()):
                if node in connection:
                    del self.connections[connection]
            print("Node '{}' removed.".format(node))
        else:
            print("Node with data '{}' does not exist.".format(node))

    def addEdge(self, v1, v2, weight):
        self.connections[(v1, v2)] = weight

    def removeEdge(self, v1, v2):
        # Removes the edge between vertices v1 and v2
        if (v1, v2) in self.connections:
            del self.connections[(v1, v2)]
        else:
            print("Edge between '{}' and '{}' does not exist.".format(v1, v2))

    def importFromFile(self, file):
        # Clear existing vertices and connections
        self.vertices = {}
        self.connections = {}

        try:
            with open(file, 'r') as f:
                lines = f.readlines()

                # Check if the file starts with 'strict graph G'
                if len(lines) < 1 or not lines[0].startswith('strict graph'):
                    print("Invalid file format.")
                    return None

                # Parse each line for edges
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith('}'):
                        break  # End of graph description
                    elif line and not line.startswith('//'):  # Ignore comments
                        parts = line.split('--')
                        if len(parts) == 2:
                            # Extract vertex names
                            vertex1, vertex2 = parts[0].strip().rstrip(';'), parts[1].split('[')[0].strip().rstrip(';')
                            weight = 1  # Default weight
                            # Extract weight if available
                            if '[' in line:
                                weight_part = line.split('[')[1].split(']')[0]
                                weight_str = weight_part.split('=')[1].strip()
                                weight = int(weight_str)
                            # Add vertices and edges to the graph
                            self.addNode(vertex1)
                            self.addNode(vertex2)
                            self.addEdge(vertex1, vertex2, weight)
        except FileNotFoundError:
            print("File not found:", file)
            return None
        except Exception as e:
            print("Error:", e)
            return None        

graph = Graph()
graph.importFromFile("graph_description.txt")

# Print vertices
print("Vertices:")
for vertex in graph.vertices:
    print(vertex)

# Print edges
print("\nEdges:")
for connection, weight in graph.connections.items():
    print(connection[0], "--", connection[1], "[weight={}];".format(weight))
