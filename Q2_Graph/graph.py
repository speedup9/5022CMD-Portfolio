class Graph:
    """Generic unweighted directed graph (adjacency list).

    Vertices can be any hashable object, so this class has no
    course-specific code and can be reused in other programs.
    """

    def __init__(self):
        # key = vertex, value = list of vertices it points TO (outgoing edges)
        self.adjacency = {}

    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self.adjacency:
            return False
        self.adjacency[vertex] = []
        return True

    def addEdge(self, source, destination):
        """Add a directed edge source -> destination.
        Returns False if a vertex is missing, the edge already exists,
        or source and destination are the same vertex."""
        if source not in self.adjacency or destination not in self.adjacency:
            return False
        if source == destination or destination in self.adjacency[source]:
            return False
        self.adjacency[source].append(destination)
        return True

    def removeEdge(self, source, destination):
        """Remove the edge source -> destination. Returns False if it doesn't exist."""
        if source in self.adjacency and destination in self.adjacency[source]:
            self.adjacency[source].remove(destination)
            return True
        return False

    def listIncomingAdjacentVertex(self, vertex):
        """List all vertices that have an edge pointing INTO the given vertex."""
        incoming = []
        for other, neighbours in self.adjacency.items():
            if vertex in neighbours:
                incoming.append(other)
        return incoming

    def listOutgoingAdjacentVertex(self, vertex):
        """List all vertices the given vertex has an edge pointing TO."""
        return list(self.adjacency.get(vertex, []))

    def getVertices(self):
        """Return a list of all vertices."""
        return list(self.adjacency.keys())


if __name__ == "__main__":
    g = Graph()
    for v in ["A", "B", "C"]:
        g.addVertex(v)
    g.addEdge("A", "C")
    g.addEdge("B", "C")
    print("Incoming to C:", g.listIncomingAdjacentVertex("C"))   # ['A', 'B']
    print("Outgoing from A:", g.listOutgoingAdjacentVertex("A")) # ['C']
