import random
import sys
import itertools as it
import matplotlib.pyplot as plt
import networkx as nx
from steinlib.instance import SteinlibInstance
from steinlib.parser import SteinlibParser
from state import State

# stein_file = "data/test.std"
stein_file = "data/B/b02.stp"


def annealing(state):
    for _ in range(200):
        state = optimize(state)
        print(state)
    return state


def optimize(state):
    old_sol = []
    for e in state.sol:
        old_sol.append(e)
    old_score = state.score
    state.random_action()
    if old_score < state.score:
        return State(state.graph, state.terms, old_sol)
    else:
        return state


def get_sol_list(graph):
    res = []
    for e in graph.edges:
        res.append((e[0], e[1]))
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
        # print ("weight: " + str(weight))
        self.my_graph.add_edge(e_start, e_end, weight=weight)


if __name__ == "__main__":
    my_class = MySteinlibInstance()
    with open(stein_file) as my_file:
        my_parser = SteinlibParser(my_file, my_class)
        my_parser.parse()
        my_terms = my_class.terms
        my_graph = my_class.my_graph
        my_sol = get_sol_list(my_graph)

        my_state = State(my_graph, my_terms, my_sol)
        my_state = annealing(my_state)
        my_state.print_graph()

# comparer two parameters with interval, confidence
