# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
from csv import Dialect
from signal import SIG_DFL
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
"""    
Each line in the text file holds 4 numbers: (start building, end building, distance, outdoor distance)
- instanciate a new Diagraph object
- loop over the text file and for each line instanciate check if start and endbuilding
    already have been added as nodes to the graph, if not add them and second 
    add the weighted edge to the start building node.
"""


# Problem 2b: Implementing load_map
def load_map(map_filename):
    digraph = Digraph()

    print("Loading map from file...")
    
    campus_data = open(map_filename, 'r', encoding='utf-8')
    with campus_data:
        for line in campus_data:
            array = line.split(' ')
            src_node = Node(array[0])
            dest_node = Node(array[1])
            if src_node not in digraph.edges:
                digraph.add_node(src_node)
            if dest_node not in digraph.edges:
                digraph.add_node(dest_node)
            edge = WeightedEdge(src_node, dest_node, int(array[2]), int(array[3]))
            digraph.add_edge(edge)
    print("finished")
    return digraph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
def test_load_map():
    digraph = load_map('test_load_map.txt')
    digraph_test = Digraph()
    node1 = Node('1')
    node2 = Node('2')
    node3 = Node('3')
    node4 = Node('4')
    digraph_test.add_node(node1)
    digraph_test.add_node(node2)
    digraph_test.add_node(node3)
    digraph_test.add_node(node4)
    edge1 = WeightedEdge(node1, node2, 70, 30)
    edge2 = WeightedEdge(node2, node3, 70, 5)
    edge3 = WeightedEdge(node1, node3, 30, 10)
    edge4 = WeightedEdge(node1, node4, 30, 10)
    digraph_test.add_edge(edge1)
    digraph_test.add_edge(edge2)
    digraph_test.add_edge(edge3)
    digraph_test.add_edge(edge4)
    return (digraph.__str__() == digraph_test.__str__())
    

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
"""
Goal is to find a function that returns the shortest (= least amount of meters) possible path from A to B. Constraint 
might be a max. amount of meters outside
"""

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path,  best_path, max_dist_outdoors, best_dist):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    path = [path[0] + [start]]
    if len(path) < 2:
        path.append(0)
    if(start == end):
        return path
    start_node = Node(start)
    edges = digraph.get_edges_for_node(start_node)
    for edge in edges:
        start = edge.get_destination().get_name()
        if(start not in path):
            if best_path == None or path[1] <  best_dist:
                path[1] += edge.get_total_distance()
                new_path = get_best_path(digraph, edge.get_destination().get_name(), end, path, best_path, max_dist_outdoors, best_dist)
                if new_path != None:
                    best_path = new_path
    return best_path


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    pass


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    #unittest.main()
    #digraph = load_map("test_load_map.txt")
    digraph = load_map("PS2/test_load_map.txt")
    #print(digraph.__str__())
    #print(test_load_map())
    #print(digraph.__str__())
    print(get_best_path(digraph, "4", "6", [[]], None, 0, 0))
