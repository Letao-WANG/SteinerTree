import random
import networkx as nx
import matplotlib.pyplot as plt


class State(object):
    """
    This class represents the state of graph
    """

    def __init__(self, graph, terms: [], sol: [], temperature: float, speed: float):
        """
        graph: nx.Graph()
        terms: the nodes list we want to span (parcours)
        sol: the edges list to span terms. ATTENTION! it is equal to "selected edges"
        temperature: parameter of simulated annealing algorithm, amplitude to optimize
        speed: parameter of simulated annealing algorithm, speed reduce temperature
        """
        self.graph = graph
        self.terms = terms
        self.sol = sol
        self.temperature = temperature
        self.speed = speed

    def __repr__(self):
        res = "score :" + str(self.score) + ", temperature: " + str(self.temperature)
        return res

    @property
    def selected_nodes(self):
        res = []
        for e in self.sol:
            if e[0] not in res:
                res.append(e[0])
            if e[1] not in res:
                res.append(e[1])
        return res

    @property
    def unselected_nodes(self):
        return list(set(self.graph.nodes) - set(self.selected_nodes))

    @property
    def score(self):
        """
        Evaluation function for the graph state
        """
        cost = self.graph_sol.size(weight='weight')
        cost += self.number_not_covered_terminals * 100
        cost += self.number_components * 100
        return int(cost)

    @property
    def graph_sol(self):
        graph_sol = nx.Graph()
        for (i, j) in self.sol:
            graph_sol.add_edge(i, j, weight=self.graph[i][j]['weight'])
        return graph_sol

    @property
    def number_not_covered_terminals(self):
        number = 0
        for i in self.terms:
            if i not in self.graph_sol:
                number = number + 1
        return number

    @property
    def number_components(self):
        number = 0
        number_components = nx.number_connected_components(self.graph_sol)
        for _ in range(number_components - 1):
            number = number + 1
        return number

    def get_neighbor_edges(self, node: int):
        """
        return the neighbor list of the node
        """
        neighbor_list = []
        for edge in self.sol:
            if node in edge:
                neighbor_list.append(edge)
        return neighbor_list

    def random_node_action(self):
        """
        do a random node action, delete a selected node, or add a unselected node
        """
        decision = random.randint(0, 1)
        if decision == 0:
            self.delete_random_node()
        else:
            self.add_random_node()
        if self.temperature > 0.0:
            self.temperature = self.temperature - self.speed

    def delete_random_node(self):
        selected_not_terms_nodes = list(set(self.selected_nodes) - set(self.terms))
        if len(selected_not_terms_nodes) > 0:
            node_delete = random.choice(selected_not_terms_nodes)
            neighbor_edges = self.get_neighbor_edges(node_delete)
            for edge in neighbor_edges:
                if edge in self.sol:
                    self.sol.remove(edge)

    def add_random_node(self):
        if len(self.graph.edges) > len(self.sol):
            not_selected_edges = list(set(self.graph.edges) - set(self.sol))
            edge_add = random.choice(not_selected_edges)
            self.sol.append(edge_add)

    def random_edge_action(self):
        """
        do a random edge action, delete a selected edge or add an unselected edge
        """
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

    def print_graph(self):
        """
        print the graphic state
        """
        pos = nx.kamada_kawai_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        if not (self.terms is None):
            nx.draw_networkx_nodes(self.graph, pos, nodelist=self.terms, node_color='r')
        if not (self.sol is None):
            nx.draw_networkx_edges(self.graph, pos, edgelist=self.sol, edge_color='r')
        plt.show()
        return
