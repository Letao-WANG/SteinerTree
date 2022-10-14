import random
import sys
import itertools as it
import matplotlib.pyplot as plt
import networkx as nx
from steinlib.instance import SteinlibInstance
from steinlib.parser import SteinlibParser

# stein_file = "data/test.std"
stein_file = "data/B/b02.stp"


# draw a graph in a window
def print_graph(graph, terms=None, sol=None):
    pos = nx.kamada_kawai_layout(graph)

    nx.draw(graph, pos, with_labels=True)
    if (not (terms is None)):
        nx.draw_networkx_nodes(graph, pos, nodelist=terms, node_color='r')
    if (not (sol is None)):
        nx.draw_networkx_edges(graph, pos, edgelist=sol, edge_color='r')
    plt.show()
    return


# verify if a solution is correct and evaluate it
def eval_sol(graph, terms, sol):
    graph_sol = nx.Graph()
    for (i, j) in sol:
        graph_sol.add_edge(i, j, weight=graph[i][j]['weight'])

    # is sol a tree
    if (not (nx.is_tree(graph_sol))):
        print("Error: the proposed solution is not a tree")
        return -1

    # are the terminals covered
    for i in terms:
        if not i in graph_sol:
            print("Error: a terminal is missing from the solution")
            return -1

    # cost of solution
    cost = graph_sol.size(weight='weight')

    return int(cost)


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
    # The complete graph of terminals
    comp_graph = nx.complete_graph(terms)
    # Add weight to the edges
    for e in comp_graph.edges:
        comp_graph[e[0]][e[1]]['weight'] = len_path[e[0]][0][e[1]]
    # The minimum spanning tree of the complete graph
    min_span_tree = nx.minimum_spanning_tree(comp_graph)
    res = []
    # path to edges
    for e in min_span_tree.edges:
        for i in range(len(len_path[e[0]][1][e[1]]) - 1):
            res.append((len_path[e[0]][1][e[1]][i],
                        len_path[e[0]][1][e[1]][i + 1]))
    # return a list of edges
    return res


def algo_naive(graph, terms, sol):
    old_selected_edge = random.choice(sol)
    not_selected_edge = random.choice(list(set(graph) - set(sol)))
    sol = exchange_selected(old_selected_edge, not_selected_edge, graph, sol)
    score = eval_sol(graph, terms, sol)
    print(score)
    return score


def exchange_selected(old_edge, new_edge, graph, sol):
    """
    exchange a selected edge and a non-selected edge, exchange means change them in variable sol.
    :param old_edge: old selected edges of type (int, int)
    :param new_edge: new selected edges of type (int, int)
    :param graph: Graph
    :param sol: list of edges of type (int, int)
    :return: sol

    :TODO: optimize code style with throw exception, and verif it works
    """
    if old_edge in sol:
        sol.remove(old_edge)
        if new_edge in graph.edges:
            sol.appand(new_edge)
        else:
            print("Error! new edge not in graph")
    else:
        print("Error! old edge not in sol")
    return sol


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

        my_sol = approx_steiner(my_graph, my_terms)
        print_graph(my_graph, my_terms, my_sol)
        print(eval_sol(my_graph, my_terms, my_sol))
        # algo_naive(graph, terms, my_sol)

# comparer two parameters with interval, confidence
