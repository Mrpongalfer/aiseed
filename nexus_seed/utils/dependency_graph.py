import networkx as nx
import matplotlib.pyplot as plt
from typing import Any

class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_dependency(self, service: str, dependency: str) -> None:
        try:
            self.graph.add_edge(service, dependency)
            print(f"Added dependency: {service} -> {dependency}")
        except Exception as e:
            print(f"Error adding dependency: {e}")

    def visualize(self) -> None:
        try:
            nx.draw(self.graph, with_labels=True)
            plt.show()
        except Exception as e:
            print(f"Error visualizing dependency graph: {e}")
