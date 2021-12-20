import heapq
import numpy as np
import io
import argparse

class Node():
    def __init__(self, node, distance):
        self.node = node
        self.distance = distance
    def __lt__(self, other):
        return self.distance.get(self.node, np.inf) < self.distance.get(other.node, np.inf)
    def __gt__(self, other):
        return self.distance.get(self.node, np.inf) > self.distance.get(other.node, np.inf)
    def __le__(self, other):
        return self.distance.get(self.node, np.inf) <= self.distance.get(other.node, np.inf)
    def __ge__(self, other):
        return self.distance.get(self.node, np.inf) >= self.distance.get(other.node, np.inf)
    def __ne__(self, other):
        return self.distance.get(self.node, np.inf) != self.distance.get(other.node, np.inf)
    def __eq__(self, other):
        return self.distance.get(self.node, np.inf) == self.distance.get(other.node, np.inf)

def dijkstra_slow(start, destination, nodes, edges, weights):
    visited = set()
    distances = {node : np.inf for node in nodes}
    previous = {}
    distances[start] = 0
    current_node = start
    while True:
        neighbors = edges[current_node]
        for neighbor in neighbors:
            if neighbor not in visited:
                distance = weights[neighbor] + distances[current_node]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
        visited.add(current_node)
        if destination in visited:
            # finished
            return distances, previous
        elif np.min([distances[node] for node in nodes if node not in visited]) == np.inf:
            # no path
            raise Exception(f"no path from {start} to {destination}")
        min_dist = np.inf
        min_dist_node = None
        for node in nodes:
            if node not in visited and distances[node] < min_dist:
                min_dist = distances[node]
                min_dist_node = node
        current_node = min_dist_node

def dijkstra(start, destination, nodes, edges, weights):
    visited = set()
    distances = {node : np.inf for node in nodes}
    previous = {}
    distances[start] = 0
    
    open_set = []
    heapq.heappush(open_set, Node(start, distances))

    while True:
        current_node = heapq.heappop(open_set).node

        neighbors = edges[current_node]
        for neighbor in neighbors:
            if neighbor not in visited:
                distance = weights[neighbor] + distances[current_node]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(open_set, Node(neighbor, distances))

        visited.add(current_node)
        if destination in visited:
            # finished
            return distances, previous

    raise Exception(f"no path from {start} to {destination}")

def a_star(start, destination, nodes, edges, weights, heuristic):
    previous = {}
    
    g = {node : np.inf for node in nodes}
    g[start] = 0
    f = {node : np.inf for node in nodes}
    f[start] = heuristic(start)

    open_set = []
    heapq.heappush(open_set, Node(start, f))

    while len(open_set) > 0:
        current_node = heapq.heappop(open_set).node

        neighbors = edges[current_node]
        for neighbor in neighbors:
            distance = g[current_node] + weights[neighbor]
            if distance < g[neighbor]:
                previous[neighbor] = current_node
                g[neighbor] = distance
                f[neighbor] = distance + heuristic(neighbor)
                if neighbor not in open_set:
                    heapq.heappush(open_set, Node(neighbor, f))
        
        if current_node == destination:
            # finished
            return g, previous

    raise Exception(f"no path from {start} to {destination}")

def print_path(nodes, weights, path):
    height = max([n[0] for n in nodes]) + 1
    width = max([n[1] for n in nodes]) + 1
    for i in range(height):
        for j in range(width):
            if (i, j) in path:
                print("\N{ESC}[31m" + f"{weights[(i, j)]}" + "\u001b[0m", end="")
            else:
                print(f"{weights[(i, j)]}", end="")
        print("")
    print("")

def make_graph(lines):
    nodes = set()
    weights = dict()
    edges = dict()
    for i, line in enumerate(lines):
        for j, risk in enumerate(line):
            nodes.add((i, j))
            weights[(i, j)] = int(risk)

            node_edges = []
            if j < len(line) - 1:
                node_edges.append((i, j + 1))
            if i < len(lines) - 1:
                node_edges.append((i + 1, j))
            if j > 0:
                node_edges.append((i, j - 1))
            if i > 0:
                node_edges.append((i - 1, j))
            edges[(i, j)] = node_edges
    
    return nodes, weights, edges

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--use-a-star", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose
    use_a_star = args.use_a_star

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    nodes, weights, edges = make_graph(lines)

    height = max([n[0] for n in nodes]) + 1
    width = max([n[1] for n in nodes]) + 1

    start = (0, 0)
    dest = (height - 1, width - 1)
    if use_a_star:
        distances, previous = a_star(start, dest, nodes, edges, weights, heuristic=lambda x : min([x[0], x[1]]))
    else:
        distances, previous = dijkstra(start, dest, nodes, edges, weights)
    
    path = []
    current = dest
    while current is not None:
        path.append(current)
        current = previous.get(current, None)
    
    if verbose:
        print_path(nodes, weights, path)
    
    print("Total risk:", sum([weights[p] for p in path]) - weights[start])

if __name__ == "__main__":
    main()
