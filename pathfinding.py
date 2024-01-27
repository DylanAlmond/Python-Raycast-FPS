from collections import deque

# Breadth first search pathfinding algorithm
class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        # W, N, E, S, NW, NE, SE, SW
        self.dir = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            # can break if pathfinding invalid on map change
            try:
                next_nodes = graph[cur_node]
            except:
                continue

            # Check if node not already in queue
            for node in next_nodes:
                if node not in visited and node not in self.game.handler.npc_positions:
                    queue.append(node)
                    visited[node] = cur_node

        return visited

    def get_next_nodes(self, x ,y):
        return [(x + dx, y + dy) for dx, dy in self.dir if (x + dx, y + dy) not in self.game.map.world_map]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)