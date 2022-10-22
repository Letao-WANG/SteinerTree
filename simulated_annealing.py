import random
import sys
import itertools as it
import matplotlib.pyplot as plt
import math
import networkx as nx
from steinlib.instance import SteinlibInstance
from steinlib.parser import SteinlibParser
from state import State

# stein_file = "data/test.std"
stein_file = "data/B/b02.stp"


def annealing(state: State, times: int):
    """
    Simulated annealing algorithm
    """
    points_x = []
    points_y = []
    for i in range(times):
        state = optimize(state)
        if i % 100 == 0:
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
        my_sol = get_sol_list(my_graph)

        # execute simulated annealing algorithm
        my_state = State(my_graph, my_terms, my_sol, temperature=20.0, speed=0.002)
        final_state, point_x, point_y = annealing(my_state, 10000)

        # print the result
        print(final_state)
        plt.plot(point_x, point_y)
        plt.show()
