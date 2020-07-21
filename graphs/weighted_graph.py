from graphs.graph import Graph, Vertex


class WeightedVertex(Vertex):

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.id = vertex_id
        self.neighbors_dict = {}  # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor by storing it in the neighbors dictionary.
        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (number): The weight of this edge.
        """
        if vertex_obj.get_id() in self.neighbors_dict.keys():
            return  # it's already a neighbor

        self.neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return [neighbor for (neighbor, weight) in self.neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex."""
        return list(self.neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id


class WeightedGraph(Graph):

    INFINITY = float('inf')

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.
        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {}
        self.is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.
        Returns:
        Vertex: The new vertex object.
        """
        if vertex_id in self.vertex_dict.keys():
            return False  # it's already there
        vertex_obj = WeightedVertex(vertex_id)
        self.vertex_dict[vertex_id] = vertex_obj
        return True

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.vertex_dict.keys():
            return None
        vertex_obj = self.vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.
        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        weight (number): The edge weight.
        """
        all_ids = self.vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)

    def get_vertices(self):
        """Return all the vertices in the graph"""
        return list(self.vertex_dict.values())

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax:
        for vertex in graph"""
        return iter(self.vertex_dict.values())

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root

    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if (parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of 
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # Create a list of all edges in the graph, sort them by weight
        # from smallest to largest
        edges = list()
        seen_edges = set()
        for vertex_obj in self.get_vertices():
            for neighbor_obj in vertex_obj.get_neighbors_with_weights():
                neighbor, weight = neighbor_obj
                vertex_id = vertex_obj.get_id()
                neighbor_id = neighbor.get_id()
                if (vertex_id, neighbor_id) not in seen_edges and (neighbor_id, vertex_id) not in seen_edges:
                    edges.append((weight, vertex_id, neighbor_id))
                    seen_edges.add((vertex_id, neighbor_id))
        edges = sorted(edges)

        parent_map = dict()
        for vertex in self.vertex_dict:
            parent_map[vertex] = vertex

        spanning_tree = list()
        index = 0
        while len(spanning_tree) < len(self.get_vertices()) - 1:
            weight, v1, v2 = edges[index]
            if self.find(parent_map, v1) != self.find(parent_map, v2):
                spanning_tree.append((v1, v2, weight))
                self.union(parent_map, v1, v2)
            else:
                index += 1

        # Return the solution list.
        return spanning_tree

    def minimum_spanning_tree_prim(self):
        vertex_to_weight = {}
        vertices = self.vertex_dict
        for vertex in vertices:
            vertex_to_weight[vertex] = WeightedGraph.INFINITY

        current_id = list(self.vertex_dict.keys())[0]
        vertex_to_weight[current_id] = 0

        mst_weight = 0

        while len(vertex_to_weight)-1 > 0:
            current_obj = self.get_vertex(current_id)
            neighbors = current_obj.get_neighbors_with_weights()
            vertex_to_weight.pop(current_id)

            for neighbor in neighbors:
                neighbor_id, neighbor_weight = neighbor[0].get_id(
                ), neighbor[1]
                if neighbor_id in vertex_to_weight:
                    if neighbor_weight < vertex_to_weight[neighbor_id]:
                        vertex_to_weight[neighbor_id] = neighbor_weight

            min_weight = WeightedGraph.INFINITY
            min_id = None
            for v_id, v_weight in zip(vertex_to_weight.keys(), vertex_to_weight.values()):
                v_weight = vertex_to_weight[v_id]
                if v_weight < min_weight:
                    min_weight = v_weight
                    min_id = v_id
            mst_weight += min_weight
            current_id = min_id

        return mst_weight

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight of the shortest path
        from a start vertex to a destination.
        """
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_distance = {i.get_id(): float("inf") for i in self.get_vertices()}
        vertex_to_distance[start_id] = 0

        # 1. Get the minimum-distance remaining vertex, remove it from the
        #    dictionary. If it is the target vertex, return its distance.
        # 2. Update that vertex's neighbors by adding the edge weight to the
        #    vertex's distance, if it is lower than previous.
        while(vertex_to_distance):
            bestVert = (start_id, float("inf"))
            for vert_id, dist in vertex_to_distance.items():
                if dist < bestVert[1]:
                    bestVert = (vert_id, dist)
            if(bestVert[0] == target_id):
                return bestVert[1]

            del vertex_to_distance[bestVert[0]]
            for neighbor, weight in self.get_vertex(bestVert[0]).get_neighbors_with_weights():
                if(neighbor in vertex_to_distance):
                    vertex_to_distance[neighbor] = min(vertex_to_distance[neighbor], weight + bestVert[1])
        return None

    def floyd_warshall(self):
        """
        Return the All-Pairs-Shortest-Paths dictionary, containing the shortest
        paths from each vertex to each other vertex.
        """
        
        dist = {}
        vertex_ids = self.vertex_dict.keys()
        
        # Create a dictionary of all vertices and their possible connections
        for v1 in vertex_ids:
            dist[v1] = dict()
            for v2 in vertex_ids:
                dist[v1][v2] = WeightedGraph.INFINITY
            dist[v1][v1] = 0
        
        # Add all edge weights to the dict
        vertices = self.get_vertices()
        
        for vertex in vertices:
            weighted_neighbors = vertex.get_neighbors_with_weights()
            
            for neighbor, weight in weighted_neighbors:
                dist[vertex.get_id()][neighbor.get_id()] = weight
        
        for i in vertices:
            for j in vertices:
                for k in vertices:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                    
        return dist