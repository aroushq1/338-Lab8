import heapq
import time

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

    def slowSP(self, source):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[source] = 0
        visited = set()

        start_time = time.time()

        while len(visited) < len(self.vertices):
            min_distance = float('inf')
            min_vertex = None

            for vertex in self.vertices:
                if vertex not in visited and distances[vertex] < min_distance:
                    min_distance = distances[vertex]
                    min_vertex = vertex

            if min_vertex is None:
                break

            visited.add(min_vertex)

            for neighbor in self.vertices[min_vertex].getNeighbors():
                weight = self.connections.get((min_vertex, neighbor), float('inf'))
                new_distance = distances[min_vertex] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

        end_time = time.time()

        return end_time - start_time

    def fastSP(self, source):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[source] = 0
        visited = set()

        start_time = time.time()

        pq = [(0, source)]

        while pq:
            dist, vertex = heapq.heappop(pq)

            if vertex in visited:
                continue

            visited.add(vertex)

            for neighbor in self.vertices[vertex].getNeighbors():
                weight = self.connections.get((vertex, neighbor), float('inf'))
                new_distance = dist + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))

        end_time = time.time()

        return end_time - start_time

# Create graph and import data from file
graph = Graph()
graph.importFromFile("random.dot")

# Debug: Print the vertices and connections to verify graph initialization
print("Vertices:", graph.vertices)
print("Connections:", graph.connections)

# Measure the performance of slowSP
slow_times = []
for vertex in graph.vertices:
    slow_time = graph.slowSP(vertex)
    print(f"SlowSP time for {vertex}: {slow_time}")  # Debug: Print slowSP times
    slow_times.append(slow_time)

# Debug: Print slow_times to verify if it's being populated
print("SlowSP times:", slow_times)

# Measure the performance of fastSP
fast_times = []
for vertex in graph.vertices:
    fast_time = graph.fastSP(vertex)
    fast_times.append(fast_time)

# Debug: Print fast_times to verify if it's being populated
print("FastSP times:", fast_times)

# Calculate statistics only if the arrays are not empty
if slow_times:
    slow_avg_time = sum(slow_times) / len(slow_times)
    slow_max_time = max(slow_times)
    slow_min_time = min(slow_times)

if fast_times:
    fast_avg_time = sum(fast_times) / len(fast_times)
    fast_max_time = max(fast_times)
    fast_min_time = min(fast_times)

# Report results
print("SlowSP:")
print("Average time:", slow_avg_time)
print("Max time:", slow_max_time)
print("Min time:", slow_min_time)

print("\nFastSP:")
print("Average time:", fast_avg_time)
print("Max time:", fast_max_time)
print("Min time:", fast_min_time)

# Plot histogram
import matplotlib.pyplot as plt

plt.hist(slow_times, bins=10, alpha=0.5, label='slowSP')
plt.hist(fast_times, bins=10, alpha=0.5, label='fastSP')
plt.legend(loc='upper right')
plt.show()

'''
The comparison showed fastSP being much faster. slowSP used a linear search approach, 
resulting in longer execution times, whereas fastSP utilized a priority queue, enabling 
more efficient selection of nodes with minimal distances.
'''