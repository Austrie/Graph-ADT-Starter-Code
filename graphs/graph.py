from collections import deque
from operator import itemgetter
import random

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.get_id()] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = dict() # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        new_vertex = Vertex(vertex_id)
        self.__vertex_dict[vertex_id] = new_vertex
        return new_vertex
        

    def get_vertex(self, vertex_id) -> Vertex:
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        vertex_1 = self.__vertex_dict[vertex_id1]
        vertex_2 = self.__vertex_dict[vertex_id2]
        vertex_1.add_neighbor(vertex_2)
        if not self.__is_directed:
            vertex_2.add_neighbor(vertex_1)
        
    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.pop()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return seen # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque() 
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        distance_dict = {}
        self.__find_vertices_n_away_helper__(start_id, target_distance, 0, distance_dict)
        return [
            key
            for key, value in distance_dict.items()
            if value == target_distance
        ]


    def __find_vertices_n_away_helper__(self, start_id,
        target_distance: int, curr_distance: int, distance_dict: dict):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for
        seen (Set): A set containing ids that you wanted excluded from this call's result.

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        if start_id not in distance_dict or distance_dict[start_id] > curr_distance:
                distance_dict[start_id] = curr_distance
        if target_distance == curr_distance: 
            return

        curr_vertex_obj: Vertex = self.get_vertex(start_id)
        for neighbor_vertex_obj in curr_vertex_obj.get_neighbors():
            neighbor_vertex_id = neighbor_vertex_obj.get_id()
            self.__find_vertices_n_away_helper__(
                neighbor_vertex_id, target_distance, curr_distance + 1, distance_dict
            )


    def __get_entry_points__(self, if_not_directed_return_one=True, return_all_values_too=False):
        if not self.__is_directed:
            if if_not_directed_return_one:
                startable_ids = [list(self.__vertex_dict.keys())[0]]
            else:
                startable_ids = list(self.__vertex_dict.keys())
        else:
            startable_ids = set(self.__vertex_dict.keys())
            all_values = set()
            for starting_id in startable_ids:
                neighbors_arr = [neighbor_vertex.get_id() for neighbor_vertex in self.__vertex_dict[starting_id].get_neighbors()]
                all_values.update(neighbors_arr)
            startable_ids = list(startable_ids - all_values)

        return startable_ids if not return_all_values_too else (startable_ids, list(all_values))

    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        startable_ids = self.__get_entry_points__()

        is_actually_bipartite = False
        for start_id in startable_ids:
            next_try = False
            # Keep a set to denote which vertices we've seen before
            red_seen = set()
            red_seen.add(start_id)
            blue_seen = set()

            # Keep a queue so that we visit vertices in the appropriate order
            queue = deque()
            queue.append(self.get_vertex(start_id))

            current_color_blue = True
            # print('Current color is:', "blue" if current_color_blue else "red")
            while queue and not next_try:
                current_vertex_obj = queue.pop()
                # current_vertex_id = current_vertex_obj.get_id()

                # Process current node
                # print('Processing neighbors of vertex {}'.format(current_vertex_id))
                # print("Neighbors are", [neighbor.get_id() for neighbor in current_vertex_obj.get_neighbors()])
                # print('Color to be assigned to neighbors is:', "blue" if current_color_blue else "red")

                # Add its neighbors to the queue
                for neighbor in current_vertex_obj.get_neighbors():
                    neighbor_id = neighbor.get_id()
                    if neighbor_id in red_seen:
                        if current_color_blue:
                            next_try = True
                            break
                    elif neighbor_id in blue_seen:
                        if not current_color_blue:
                            next_try = True
                            break
                    else:
                        if current_color_blue:
                            blue_seen.add(neighbor_id)
                        else:
                            red_seen.add(neighbor_id)
                        queue.append(neighbor)
                current_color_blue = not current_color_blue
            if not next_try:
                is_actually_bipartite = True
                break

        # print("blue_seen:", blue_seen)
        # print("red_seen:", red_seen)
        # print('is_actually_bipartite:', is_actually_bipartite)
        return is_actually_bipartite

    def get_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        # startable_ids, all_values = self.__get_entry_points__(True, True)
        all_values = set(self.__vertex_dict.keys())

        all_seen = {}
        components = {}
        curr_component = -1
        for start_id in all_values:
            if start_id in all_seen:
                continue

            curr_component += 1
            temp_component = None
            components[curr_component] = set()
            curr_vertex_obj = self.get_vertex(start_id)
            queue = deque()
            queue.append(curr_vertex_obj)
            while queue:
                current_vertex_obj = queue.pop()
                curr_id = current_vertex_obj.get_id()
                if curr_id in all_seen:
                    correct_component = all_seen[curr_id]
                    if correct_component == curr_component:
                        continue
                    components[correct_component].update(
                        components[curr_component]
                    )
                    components[correct_component].add(curr_id)
                    for id in components[curr_component]:
                        all_seen[id] = correct_component
                    
                    temp_component = curr_component
                    curr_component = correct_component
                    # components.pop(curr_component, None)
                    components[temp_component] = set()
                else:
                    all_seen[curr_id] = curr_component
                    components[curr_component].add(curr_id)
                # Process current node
                # print('Processing neighbors of vertex {}'.format(current_vertex_obj.get_id()))
                # print("Neighbors are", [neighbor.get_id() for neighbor in current_vertex_obj.get_neighbors()])

                # Add its neighbors to the queue
                for neighbor in current_vertex_obj.get_neighbors():
                    queue.append(neighbor)
            curr_component = temp_component - 1 if temp_component else curr_component
            temp_component = None

        return [list(components[component_key]) for component_key in components if len(components[component_key]) > 0]

    
    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # stack of vertices to visit next
        stack = list() 
        stack.append(self.get_vertex(start_id))

        # while stack is not empty
        while stack:
            current_vertex_obj = stack.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()
            # print('current_vertex_id:', current_vertex_id)
            # print('vertex_id_to_path:', vertex_id_to_path)

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            # print('Didnt break')

            neighbors = current_vertex_obj.get_neighbors()
            # print('neighbors', neighbors)
            for neighbor in neighbors:
                # if neighbor.get_id() not in vertex_id_to_path:
                current_path = vertex_id_to_path[current_vertex_id]
                # extend the path by 1 vertex
                next_path = current_path + [neighbor.get_id()]
                vertex_id_to_path[neighbor.get_id()] = next_path
                stack.append(neighbor)
                    # print(vertex_id_to_path)
            

        if target_id not in vertex_id_to_path: # path not found
            return None

        # print('vertex_id_to_path:', vertex_id_to_path)
        return vertex_id_to_path[target_id]


    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        all_components = self.get_connected_components()
        if not self.__is_directed:
            return len(all_components) > 0
        for component in all_components:
            all_neighbors = set()
            for vertex_id in component:
                all_neighbors.update(
                    [
                        vertex.get_id()
                        for vertex in self.get_vertex(vertex_id).get_neighbors()
                    ]
                )
            starting_points = list(set(component) - all_neighbors)
            if len(starting_points) == 0:
                return True
            for starting_point in starting_points:
                seen = set()
                queue = deque()
                queue.append((None, starting_point))
                while queue:
                    parent, curr_vertex_id = queue.pop()
                    if (parent, curr_vertex_id) in seen:
                        print("Cycle at:", (parent, curr_vertex_id))
                        return True
                    else:
                        seen.add(curr_vertex_id)
                        for neighbor in self.get_vertex(curr_vertex_id).get_neighbors():
                            queue.append((parent, neighbor.get_id()))

        return False


    def topological_sort_helper(
        self, dependencies, parent_priority, curr_vertex_id
    ):
        dependencies[curr_vertex_id] = (
            (
                dependencies[curr_vertex_id]
                if dependencies[curr_vertex_id] > parent_priority + 1
                else parent_priority + 1
            )
            if curr_vertex_id in dependencies else parent_priority + 1
        )
        for neighbor in self.get_vertex(curr_vertex_id).get_neighbors():
            self.topological_sort_helper(
                dependencies,
                dependencies[curr_vertex_id],
                neighbor.get_id()
            )

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """
        if self.contains_cycle():
            raise ValueError("Graph contains a cycle and/or is not a directed graph.")
        all_components = self.get_connected_components()
        dependencies = {}
        for component in all_components:
            all_neighbors = set()
            for vertex_id in component:
                all_neighbors.update(
                    [
                        vertex.get_id()
                        for vertex in self.get_vertex(vertex_id).get_neighbors()
                    ]
                )
            starting_points = list(set(component) - all_neighbors)
            for starting_point in starting_points:
                self.topological_sort_helper(dependencies, -1, starting_point)

        return [
            key
            for key, priority in sorted([
                (key, dependencies[key])
                for key in dependencies
            ], key=itemgetter(1,0))
        ]
                

