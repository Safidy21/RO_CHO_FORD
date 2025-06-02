import networkx as nx
from collections import deque

def ford_min(graph, source, order=None):
    distances = {node: float('inf') for node in graph.nodes}
    predecessors = {node: None for node in graph.nodes}
    distances[source] = 0
    steps = []
    nodes_with_lambda = {}

    if order is None:
        order = list(graph.nodes)

    order.sort(key=lambda x: (len(x), x))
    order_index = {node: idx for idx, node in enumerate(order)}
    to_process = deque(order)

    while to_process:
        i = to_process.popleft()
        neighbors = sorted(graph.neighbors(i), key=lambda x: order_index[x])
        for j in neighbors:
            weight = graph[i][j]['weight']
            old_dist_j = distances[j]
            step_entry = {
                "i": i,
                "j": j,
                "λj - λi": f"{old_dist_j} - {distances[i]} = {old_dist_j - distances[i]}",
                "v(xi, xj)": weight,
                "λj": ""
            }
            if distances[i] + weight < distances[j]:
                distances[j] = distances[i] + weight
                predecessors[j] = i
                step_entry["λj"] = f"λ({j}) = {distances[i]} + {weight} = {distances[j]}"
            nodes_with_lambda[j] = distances[j]
            steps.append(step_entry)

    return distances, predecessors, steps, nodes_with_lambda

def reconstruire_chemin(predecessors, target):
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    return path

def chemin_minimal(graph, source, target, order=None):
    if source not in graph.nodes:
        return {"error": f"Le nœud source '{source}' n'existe pas."}
    if target not in graph.nodes:
        return {"error": f"Le nœud cible '{target}' n'existe pas."}

    distances, predecessors, steps, nodes_with_lambda = ford_min(graph, source, order)
    
    if distances[target] == float('inf'):
        return {"error": f"Aucun chemin disponible vers {target} depuis {source}."}

    chemin_optimal = reconstruire_chemin(predecessors, target)
    
    return {
        "chemin": chemin_optimal,
        "steps": steps,
        "nodes_with_lambda": nodes_with_lambda
    }
