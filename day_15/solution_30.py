import numpy as np
import io
import argparse
from solution_29 import print_path, Node
import heapq

def dijkstra(start, destination, graph, get_neighbors):
    visited = set()
    distances = {}
    previous = {}
    distances[start] = 0
    
    open_set = []
    heapq.heappush(open_set, Node(start, distances))

    while len(open_set) > 0:
        current_node = heapq.heappop(open_set).node

        neighbors = get_neighbors(*current_node, *graph.shape)
        for neighbor in neighbors:
            if neighbor not in visited:
                distance = graph[neighbor] + distances[current_node]
                if distance < distances.get(neighbor, np.inf):
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(open_set, Node(neighbor, distances))
        
        visited.add(current_node)
        if destination in visited:
            # finished
            return distances, previous

    raise Exception(f"no path from {start} to {destination}")

def a_star(start, destination, graph, get_neighbors, heuristic):
    # visited = set()
    previous = {}
    
    g = {}
    g[start] = 0
    f = {}
    f[start] = heuristic(start)

    open_set = []
    heapq.heappush(open_set, Node(start, f))

    while len(open_set) > 0:
        current_node = heapq.heappop(open_set).node

        neighbors = get_neighbors(current_node)
        for neighbor in neighbors:
            distance = g[current_node] + graph[neighbor]
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

def get_neighbors(i, j, height, width):
    _neighbors = []
    if j < width - 1:
        _neighbors.append((i, j + 1))
    if i < height - 1:
        _neighbors.append((i + 1, j))
    if j > 0:
        _neighbors.append((i, j - 1))
    if i > 0:
        _neighbors.append((i - 1, j))
    return _neighbors

def make_graph_array(lines, extend_by=5):
    height = extend_by * len(lines)
    width = extend_by * len(lines[0])
    graph = np.zeros((height, width), dtype=int)
    for i, line in enumerate(lines):
        for j, risk in enumerate(line):
            for k in range(extend_by):
                for l in range(extend_by):
                    ii = i + k * int(height / extend_by)
                    jj = j + l * int(width / extend_by)
                    weight = (int(risk) - 1 + k + l) % 9 + 1
                    graph[ii, jj] = weight
    return graph

def make_graph(lines, extend_by=5):
    nodes = set()
    weights = dict()
    edges = dict()
    height = len(lines)
    width = len(lines[0])
    for i, line in enumerate(lines):
        for j, risk in enumerate(line):
            for k in range(extend_by):
                for l in range(extend_by):
                    ii = i + k * height
                    jj = j + l * width
                    nodes.add((ii, jj)) 
                    weight = (int(risk) - 1 + k + l) % 9 + 1
                    weights[(ii, jj)] = weight

                    node_edges = []
                    if jj < extend_by * len(line) - 1:
                        node_edges.append((ii, jj + 1))
                    if ii < extend_by * len(lines) - 1:
                        node_edges.append((ii + 1, jj))
                    if jj > 0:
                        node_edges.append((ii, jj - 1))
                    if ii > 0:
                        node_edges.append((ii - 1, jj))
                    edges[(ii, jj)] = node_edges
    
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
    graph = make_graph_array(lines)

    height = graph.shape[0]
    width = graph.shape[1]

    start = (0, 0)
    dest = (height - 1, width - 1)

    if use_a_star:
        distances, previous = a_star(start, dest, graph, get_neighbors, heuristic=lambda x : min([x[0], x[1]]))
    else:
        distances, previous = dijkstra(start, dest, graph, get_neighbors)
    
    path = []
    current = dest
    while current is not None:
        path.append(current)
        current = previous.get(current, None)
    
    if verbose:
        print_path(nodes, graph, path)
    
    print("Total risk:", sum([graph[p] for p in path]) - graph[start])

if __name__ == "__main__":
    main()
