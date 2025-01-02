import random
from collections import deque

class RandomPathGenerator:
    def __init__(self, path_block):
        self.size = 7
        self.blocks = [["plus.png" for _ in range(7)] for _ in range(7)]
        self.start = None
        self.middle = None
        self.end = None
        self.path_block = path_block

    def is_within_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def get_neighbours(self, pos):
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return [(x + dx, y + dy) for dx, dy in directions if self.is_within_bounds((x + dx, y + dy))]

    def bfs_path(self, start, end):
        visited = set()
        queue = deque([(start, [start])])  # Queue holds (current_position, path_taken)
        while queue:
            current, path = queue.popleft()
            if current == end:  # Found the end
                for x, y in path[1:-1]:  # Skip the start and end points
                    self.blocks[6 - y][x] = self.path_block
                return True  # Path successfully created

            for neighbour in self.get_neighbours(current):
                if neighbour not in visited and neighbour not in path:
                    visited.add(neighbour)  # Mark as visited
                    queue.append((neighbour, path + [neighbour]))

        return False  # No path found

    def generate_points(self):
        self.start = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        
        # Generate a unique middle point
        self.middle = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        while self.middle == self.start:
            self.middle = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        
        # Generate a unique end point
        self.end = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        while self.end == self.start or self.end == self.middle or abs(self.end[0]-self.middle[0]) < 1:
            self.end = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))


        print(self.start)
        print(self.middle)
        print(self.end)
        print()


        # Place the points on the grid
        self.blocks[6 - self.start[1]][self.start[0]] = self.path_block
        self.blocks[6 - self.middle[1]][self.middle[0]] = self.path_block
        self.blocks[6 - self.end[1]][self.end[0]] = "oak_trapdoor.png"

    def get_start(self):
        return self.start

    def get_blocks(self):
        return self.blocks

    def connect_points(self):
        if not self.bfs_path(self.start, self.middle):
            print("Failed to create a path from start to end")
        if not self.bfs_path(self.middle, self.end):
            print("Failed to create a path from start to end")