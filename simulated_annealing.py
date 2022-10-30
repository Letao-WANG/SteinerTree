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


def annealing(state: State, times: int, node_method=True):
    """
    Simulated annealing algorithm
    """
    points_x = []
    points_y = []
    for i in range(times):
        state = optimize(state, node_method)
        if i % 10 == 0:
            points_x.append(i)
            points_y.append(state.score)
    return state, points_x, points_y


def optimize(state: State, node_method):
    """
    Update function or function voisine
    Input an old state, output a new state with probability
    """
    old_sol = []
    for e in state.sol:
        old_sol.append(e)
    old_score = state.score
    if node_method:
        state.random_node_action()
    else:
        state.random_edge_action()
    new_score = state.score
    proba = func_proba(state, new_score, old_score)
    # proba = func_sigmoid_proba(state, new_score, old_score)
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


def func_sigmoid_proba(state, new_score, old_score):
    # let coefficient change with temperature
    coefficient = 1.0/state.temperature
    # in case the coefficient is too big
    if coefficient > 1:
        coefficient = 1
    return 1.0 / (1.0 + math.exp(coefficient * (new_score - old_score)))


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


file_name = "b07"
file = ".stp"
stein_file = "data/B/" + file_name + file

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
        my_state1 = State(my_graph, my_terms, my_sol, temperature=30.0, speed=0.01)
        final_state1, point_x1, point_y1 = annealing(my_state1, 3000)

        # execute simulated annealing algorithm
        my_state2 = State(my_graph, my_terms, my_sol, temperature=30.0, speed=0.01)
        final_state2, point_x2, point_y2 = annealing(my_state2, 3000, False)

        # # execute simulated annealing algorithm
        # my_state3 = State(my_graph, my_terms, my_sol, temperature=30.0, speed=0.01)
        # final_state3, point_x3, point_y3 = annealing(my_state3, 3000, False)
        #
        # # execute simulated annealing algorithm
        # my_state4 = State(my_graph, my_terms, my_sol, temperature=30.0, speed=0.01)
        # final_state4, point_x4, point_y4 = annealing(my_state4, 3000, False)

        print("state with node method: " + str(final_state1))
        print("state with edge method: " + str(final_state2))

        # show the graph
        plt.plot(point_x1, point_y1, color='r', label='with node method (result: ' + str(point_y1[len(point_y1)-1]) + ')')
        plt.plot(point_x2, point_y2, color='b', label='with edge method (result: ' + str(point_y2[len(point_y2)-1]) + ')')
        plt.xlabel("Number of evaluation times")
        plt.ylabel("Weights total")
        plt.title("Evaluation of two methods of algorithm simulated annealing " + str(file_name) +
                  "\n using the sigmoid probability function"
                  "\n(Tstart=30.0, speed=0.01)")
        plt.legend()
        plt.show()

        # plt.plot(point_x1, point_y1, color='r', label='with node method')
        # plt.plot(point_x1, point_y2, color='b', label='with edge method')
        # plt.xlabel("Number of evaluation times")
        # plt.ylabel("Weights total")
        # plt.title("Evaluation of two methods of algorithm simulated annealing \n(Tstart=30.0, speed=0.01)")
        # plt.legend()
        # plt.show()
