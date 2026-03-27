import networkx as nx

def dijkstra(G, start, end):
    try:
        path = nx.shortest_path(G, source=start, target=end)
        cost = nx.shortest_path_length(G, source=start, target=end)
        return path, cost
    except nx.NetworkXNoPath:
        return None, float('inf')