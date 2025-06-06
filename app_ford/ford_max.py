import networkx as nx
from collections import deque

def remove_cycles(graph):
    """
    Remove edges from cycles until the graph becomes acyclic.
    """
    G = graph.copy()
    removed_edges = []
    try_limit = 1000  # safety to avoid infinite loops
    count = 0
    while count < try_limit:
        try:
            cycle = nx.find_cycle(G, orientation='original')
            # remove last edge in cycle
            u, v, _ = cycle[-1]
            if G.has_edge(u, v):
                G.remove_edge(u, v)
                removed_edges.append((u, v))
            count += 1
        except nx.NetworkXNoCycle:
            break
    return G, removed_edges

def ford_max(graph, source, order=None):
    """
    Ford algorithm for finding the longest path in a DAG.
    Correction: We avoid removing nodes from the processing order. Instead, we mark which nodes need to be reprocessed.
    """
    # Initialize distances and predecessors
    distances = {node: 0 for node in graph.nodes}
    predecessors = {node: None for node in graph.nodes}
    distances[source] = 0
    steps = []
    nodes_with_lambda = {}

    # Determine the processing order
    if order is None:
        order = list(graph.nodes)

    # Sort order (for example: x1 < x2 < x10)
    order.sort(key=lambda x: (len(x), x))
    order_index = {node: idx for idx, node in enumerate(order)}

    # New: Use a set to track which nodes need to be processed
    to_process = deque(order)

    while to_process:

        print('order = {0}'.format(order))
        print('to_process = {0}'.format(to_process))

#        updated = deque()  # Track nodes to reprocess in the next iteration
        
        print("dans while to_process = {0}".format(to_process))

        i = to_process.popleft()
        neighbors = sorted(graph.neighbors(i), key=lambda x: order_index[x])
        for j in neighbors:
            print("Dans boucle j --- i = {0} et j = {1}".format(i, j))
            weight = graph[i][j]['weight']
            old_dist_j = distances[j]
            step_entry = {
                "i": i,
                "j": j,
                "λj - λi": f"{old_dist_j} - {distances[i]} = {old_dist_j - distances[i]}",
                "v(xi, xj)": weight,
                "λj": ""
            }
            if distances[i] + weight > distances[j]:
                distances[j] = distances[i] + weight
                predecessors[j] = i
                step_entry["λj"] = f"λ({j}) = {distances[i]} + {weight} = {distances[j]}"
#                updated.add(j)  # Mark j to be processed again
            nodes_with_lambda[j] = distances[j]
            steps.append(step_entry)

            if order_index[i] > order_index[j] and old_dist_j - distances[i] < weight:
                j_index = order.index(j)
                to_process = deque(order[j_index:])
                break
                 
            print("Dans boucle j to_process = {0}".format(to_process))
#        to_process = updated  # Only process updated nodes in the next round

    return distances, predecessors, steps, nodes_with_lambda

def reconstruire_chemin(predecessors, target):
    """
    Reconstruct the path to the target from predecessors dictionary.
    """
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    return path

def chemin_maximal(graph, source, target, order=None):
    """
    Compute the longest path using the Ford algorithm, removing cycles to avoid infinite loops.
    """
    dag, removed_edges = remove_cycles(graph)
    distances, predecessors, steps, nodes_with_lambda = ford_max(dag, source, order)

    if distances[target] == 0:
        return {"error": f"Aucun chemin disponible vers {target} depuis {source}."}

    chemin_optimal = reconstruire_chemin(predecessors, target)

    res = {
        "chemin": chemin_optimal,
        "steps": steps,
        "nodes_with_lambda": nodes_with_lambda,
        "removed_edges": [{"source": u, "target": v} for (u, v) in removed_edges]
    }
    if removed_edges:
        res["warning"] = "Cycles détectés et arcs supprimés pour éviter boucle infinie."

    return res
