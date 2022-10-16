import random
import networkx as nx
import matplotlib.pyplot as plt


class State(object):
    def __init__(self, graph, terms, sol, temperature: float, speed: float):
        self.graph = graph
        self.terms = terms
        self.sol = sol
        self.temperature = temperature
        self.speed = speed

    def __repr__(self):
        res = "score :" + str(self.score) + ", temperature: " + str(self.temperature)
        return res

    def random_action(self):
        decision = random.randint(0, 1)
        if decision == 0:
            self.delete_random_sol()
        else:
            self.add_random_sol()
        if self.temperature > 0.0:
            self.temperature = self.temperature - self.speed

    def delete_random_sol(self):
        if len(self.sol) > 0:
            edge_delete = random.choice(self.sol)
            self.sol.remove(edge_delete)

    def add_random_sol(self):
        if len(self.graph.edges) > len(self.sol):
            not_selected_edges = list(set(self.graph.edges) - set(self.sol))
            edge_add = random.choice(not_selected_edges)
            self.sol.append(edge_add)

    @property
    def score(self):
        graph_sol = nx.Graph()
        for (i, j) in self.sol:
            graph_sol.add_edge(i, j, weight=self.graph[i][j]['weight'])
        # cost of solution
        cost = graph_sol.size(weight='weight')

        # are the terminals covered
        for i in self.terms:
            if i not in graph_sol:
                cost += 50

        number_components = nx.number_connected_components(graph_sol)
        for _ in range(number_components - 1):
            cost += 50

        return int(cost)

    def print_graph(self):
        pos = nx.kamada_kawai_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        if not (self.terms is None):
            nx.draw_networkx_nodes(self.graph, pos, nodelist=self.terms, node_color='r')
        if not (self.sol is None):
            nx.draw_networkx_edges(self.graph, pos, edgelist=self.sol, edge_color='r')
        plt.show()
        return
