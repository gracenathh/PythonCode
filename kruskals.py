"""
@author: Grace Nathania
@created 30 April 2021

Kruskal's algorithm to find minimum weight spanning tree in a graph
"""

class Graph:
    """
    This class implements a Graph with an ability to create a graph, calculate the minimum
    spanning tree using Kruskal's algorithm.
    """
    def __init__(self, vertices_count, edges_file):
        """
        Construction function that initialises instances of class Graph.
        It first opening the edges file and storing it to an array
        """
        # create an array of vertices based on the number of vertex (0-N-1)
        self.vertices_count = vertices_count
        self.graph = []

        # Step 1 - Open edges_file
        file = open(edges_file, "r")

        # Step 2 - Loop through each line in file and put it into graph
        for line in file:
           u, v, w = line.strip().split()
           self.graph.append((u, v, w))

    def find(self, parent, a):
        """
        This function is used for union-find algorithm whereby we want to know
        the parent of a
        :param parent: an array of size self.vertices_count
        :param a: the "child"
        :Best complexity: O(1) if a does not belong to any tree
        :Worse complexity: O(d) with d as the level (depth) of a from its parents
        :Aux space complexity: O(N) with N as number of vertices (self.vertices_count)
        :Space complexity: O(N)
        :return a: the parents of a
        """
        if parent[a] < 0:
            return a
        else:
            parent[a] = self.find(parent[a])
            return parent[a]

    def union(self, parent, a, b):
        """
        This function performs union by height
        :param parent: an array of size self.vertices_count
        :param a: the node to be combined with b
        :param b: the node to be combined with a
        :Best complexity: O(1) if a and b do not belong to any tree
        :Worse complexity: O(d) with d as the level (depth) of a or b from its parents
        :Aux space complexity: O(N) with N as number of vertices (self.vertices_count)
        :Space complexity: O(N)
        :return: None
        """
        # Step 1 - Finding the root of a and b
        root_a = self.find(parent, a)
        root_b = self.find(parent, b)

        if root_a == root_b:
            return None

        # Step 2 - Setting the height of a and b
        height_a = -parent[root_a]
        height_b = -parent[root_b]

        # Step 3 - Performing union
        if height_a > height_b:
            parent[root_b] = root_a

        elif height_a < height_b:
            parent[root_a] = root_b

        else:
            parent[root_a] = root_b
            parent[root_b] = -(height_b + 1)

    def find_mst(self):
        """
        This function implements Kruskal's algorithm to find minimum spanning tree
        :Best complexity: O(1) when only 1 edge available in the graph
        :Worse complexity: O(N) with N as the number of vertices (self.vertices_count)
        :Aux space complexity: O(w+N) with w as the length of to_write consisting of MST weight, edge(s)
        and the length of parent (N as the number of vertices (self.vertices_count))
        :Space complexity:  O(w+N)
        :return to_write: an array consisting of MST weight and the edge(s) creating the MST
        """
        to_write = []

        e = i = 0

        # Step 1 - Sort the graph based on weight
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        mst_weight = 0

        # Step 2 - Create parent's array and append -1 since no nodes has a child yet
        for node in range(self.vertices_count):
            parent.append(-1)

        # Step 3 - "tracing" the edges and performing union to find MST
        while e < self.vertices_count - 1:
            u, v, w = self.graph[i]

            a = self.find(parent, u)
            b = self.find(parent, v)

            if a != b:
                to_write.append((u,v,w))
                self.union(parent, a, b)
                mst_weight += w # calculating the weight of MST
                e += 1

            i += 1

        to_write.insert(0, mst_weight)

        # Step 4 - return
        return to_write
