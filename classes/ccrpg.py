import random
import heapq

# Directions for neighbors (up, down, left, right)
class RandomPathGenerator:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.start = None
        self.end = None

    def generate_points(self):
        self.start = (random.randint(0, 6), random.randint(0, 6))
        self.end = (random.randint(0, 6), random.randint(0, 6))
        while self.start[0] == self.end[0] or self.start[1] == self.end[1]:
            self.end = (random.randint(0, 6), random.randint(0, 6))

    def get_start(self):
        return [self.start[1], 6-self.start[0]]

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))
        return neighbors

    def random_path(self, start, end):
        # Initialize distances to infinity and parent pointers
        distances = { (x, y): float('inf') for x in range(self.grid_size) for y in range(self.grid_size) }
        distances[start] = 0
        parents = { (x, y): None for x in range(self.grid_size) for y in range(self.grid_size) }
        
        # Priority queue (min-heap) to store the nodes to visit
        pq = [(0, start)]  # (distance, (x, y))

        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node == end:
                break
            
            # If the node has already been visited, continue
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # Get neighbors (adjacent blocks)
            neighbors = self.get_neighbors(current_node[0], current_node[1])
            
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                
                # Calculate the tentative distance to the neighbor
                new_distance = current_distance + 1  # assuming each move costs 1 (uniform grid)
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current_node
                    
                    # Add neighbor to the priority queue
                    heapq.heappush(pq, (new_distance, neighbor))
                elif new_distance == distances[neighbor]:
                    # Randomly decide between the neighbors with the same distance
                    if random.random() < 0.7:
                        parents[neighbor] = current_node
                        heapq.heappush(pq, (new_distance, neighbor))

        # Reconstruct the path
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(start)
        
        grid = [["dirt.png" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        for (x, y) in path:
            grid[x][y] = "grass_top.png"
        
        grid[self.end[0]][self.end[1]] = "oak_trapdoor.png"

        return grid
