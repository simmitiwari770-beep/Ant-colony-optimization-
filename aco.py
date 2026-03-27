import random

class ACO:
    def __init__(self, graph, ants, iterations, alpha=1.0, beta=2.0, evaporation=0.5):
        self.graph = graph
        self.ants = ants
        self.iterations = iterations
        self.alpha = alpha     # Pheromone importance
        self.beta = beta       # Distance importance
        self.evaporation = evaporation

        # Initialize base pheromones for all edges
        self.pheromone = {(u, v): 1.0 for u, v in graph.edges()}
        for u, v in list(self.pheromone.keys()):
            self.pheromone[(v, u)] = 1.0

    def run(self, start, end):
        best_cost = float('inf')
        best_path = None
        history = []

        for _ in range(self.iterations):
            paths = []

            for _ in range(self.ants):
                path, cost = self.construct_path(start, end)
                # Only keep complete valid paths
                if cost != float('inf'):
                    paths.append((path, cost))

                # Update best path
                if cost < best_cost:
                    best_cost = cost
                    best_path = path

            # Update pheromones based on the batch of paths
            self.update(paths)
            history.append(best_cost if best_cost != float('inf') else 0)

        return best_path, best_cost, history

    def construct_path(self, start, end):
        path = [start]
        visited = set(path)
        cost = 0

        current = start
        while current != end:
            neighbors = list(self.graph.neighbors(current))
            probs = []

            for n in neighbors:
                if n not in visited:
                    pher = self.pheromone.get((current, n), 1.0)
                    dist = self.graph[current][n].get('weight', 1.0)
                    
                    # Probability rule: Pheromone^alpha * (1/Distance)^beta
                    prob = (pher ** self.alpha) * ((1.0 / dist) ** self.beta)
                    probs.append((n, prob, dist))

            # If ant gets trapped, return infinity cost
            if not probs:
                cost = float('inf')
                break

            total_p = sum(x[1] for x in probs)
            if total_p == 0:
                cost = float('inf')
                break

            # Roulette wheel selection to choose next path
            rand = random.uniform(0, total_p)
            cumulative = 0
            next_node = None
            next_dist = 0
            
            for n, p, d in probs:
                cumulative += p
                if cumulative >= rand:
                    next_node = n
                    next_dist = d
                    break
            
            # Fallback
            if next_node is None:
                next_node = probs[-1][0]
                next_dist = probs[-1][2]

            path.append(next_node)
            visited.add(next_node)
            cost += next_dist
            current = next_node

        return path, cost

    def update(self, paths):
        # 1. Evaporate pheromones
        for edge in self.pheromone:
            self.pheromone[edge] *= (1.0 - self.evaporation)
            self.pheromone[edge] = max(self.pheromone[edge], 0.01)

        # 2. Deposit new pheromones from ants that found a path
        for path, cost in paths:
            deposit = 100.0 / cost 
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                self.pheromone[(u, v)] = self.pheromone.get((u, v), 0) + deposit
                self.pheromone[(v, u)] = self.pheromone.get((v, u), 0) + deposit