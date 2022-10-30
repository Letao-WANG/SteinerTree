import random
import sys
import itertools as it
import matplotlib.pyplot as plt
import math
import networkx as nx
from steinlib.instance import SteinlibInstance
from steinlib.parser import SteinlibParser

import util
from state import State

# stein_file = "data/test.std"
stein_file = "data/B/b02.stp"


def approx_steiner(graph, terms):
    """
    compute a approximate solution to the steiner problem
    Graph: graph e.g. Graph with 7 nodes and 9 edges
    List: terms e.g. [1,3,5,7]
    Dict: len_path
            e.g.
                len_path[number of vertex][distance or path][number of vertex]
                len_path[e[0]][0][e[1]]
                {1:({1:0, 2:1,...,5:2}, {1:[1], 2:[1,2],...,5:[1,4,5]}),
                2:({2:0, 1:1,...
                ...
                7}
            and we have int: weight = len_path[e[0]][0][e[1]],
                (int, int): edge = (len_path[e[0]][1][e[1]][i], len_path[e[0]][1][e[1]][i + 1])

    """
    # Find the shortest weighted paths of the original graph
    len_path = dict(nx.all_pairs_dijkstra(graph))
    # print(len_path)
    # The complete graph of terminals
    comp_graph = nx.complete_graph(terms)
    # Add weight to the edges
    for e in comp_graph.edges:
        comp_graph[e[0]][e[1]]['weight'] = len_path[e[0]][0][e[1]]
    # The minimum spanning tree of the complete graph
    min_span_tree = nx.minimum_spanning_tree(comp_graph)
    # print(min_span_tree.edges)
    res = []
    # path to edges
    for e in min_span_tree.edges:
        for i in range(len(len_path[e[0]][1][e[1]]) - 1):
            res.append((len_path[e[0]][1][e[1]][i],
                        len_path[e[0]][1][e[1]][i + 1]))
    # remove the duplicate
    res = list(set(res))
    # return a list of edges
    # print(res)
    return res


def annealing(state: State, times: int):
    """
    Simulated annealing algorithm
    """
    points_x = []
    points_y = []
    for i in range(times):
        state = optimize(state)
        if i % 10 == 0:
            points_x.append(i)
            points_y.append(state.score)
        # print(state)
    return state, points_x, points_y


def optimize(state: State):
    """
    Update function or function voisine
    Input an old state, output a new state with probability
    """
    old_sol = []
    for e in state.sol:
        old_sol.append(e)
    old_score = state.score
    state.random_edge_action()
    new_score = state.score
    proba = func_proba(state, new_score, old_score)
    if random.uniform(0, 1) < proba:
        return state
    else:
        return State(state.graph, state.terms, old_sol, state.temperature, state.speed)


def func_proba(state, new_score, old_score):
    """
    The probability to update state
    """
    if old_score >= new_score:
        return 1.0
    elif old_score < new_score:
        if state.temperature <= 0.0:
            return 0.0
        else:
            return math.exp(-(new_score - old_score) / state.temperature)


def get_sol_list(graph):
    """
    graph: nx.Graph()
    get sol (selected edges) of graph
    """
    res = []
    for e in graph.edges:
        res.append((e[0], e[1]))
    return res


def get_selected_nodes(graph):
    res = []
    for e in graph.nodes:
        res.append(e)
    return res


# class used to read a steinlib instance
class MySteinlibInstance(SteinlibInstance):
    my_graph = nx.Graph()
    terms = []

    def terminals__t(self, line, converted_token):
        self.terms.append(converted_token[0])

    def graph__e(self, line, converted_token):
        e_start = converted_token[0]
        e_end = converted_token[1]
        weight = converted_token[2]
        self.my_graph.add_edge(e_start, e_end, weight=weight)


if __name__ == "__main__":
    my_class = MySteinlibInstance()
    with open(stein_file) as my_file:

        # initialisation
        my_parser = SteinlibParser(my_file, my_class)
        my_parser.parse()
        my_terms = my_class.terms
        my_graph = my_class.my_graph
        my_sol = approx_steiner(my_graph, my_terms)

        # execute simulated annealing algorithm
        my_state = State(my_graph, my_terms, my_sol, temperature=30.0, speed=0.01)
        final_state, point_x, point_y = annealing(my_state, 3000)

        # my_state.delete_random_node()
        # my_state.delete_random_node()
        # my_state.add_random_node()

        print(final_state)
        # print(len(final_state.sol))
        # print(len(final_state.terms))
        final_state.print_graph()


        # show the graph
        plt.plot(point_x, point_y)
        plt.show()
