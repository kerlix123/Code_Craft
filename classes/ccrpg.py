import random
from collections import deque

class RandomPathGenerator:
    def __init__(self, path_block):
        self.size = 7  # Grid size (7x7)
        self.blocks = [["plus.png" for _ in range(7)] for _ in range(7)]  # Initialize all blocks
        self.start = None
        self.end = None
        self.path_block = path_block  # Path block type (e.g., "path.png")
        self.modified_blocks = set()  # Keep track of all modified blocks (path cells)

    def is_within_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def get_neighbours(self, pos):
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 possible directions
        return [(x + dx, y + dy) for dx, dy in directions if self.is_within_bounds((x + dx, y + dy))]

    def generate_valid_path(self):
        # Generate valid path from start to end
        self.start = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        self.end = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        while self.end == self.start:
            self.end = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        # Generate the path with backtracking and validation
        path = self.build_path(self.start, self.end)

        if path:
            # Mark the grid with the path
            for x, y in path:
                self.blocks[6 - y][x] = self.path_block  # Mark the grid with the path
                self.modified_blocks.add((x, y))
            return path
        else:
            print("Failed to create a valid path")
            return None

    def build_path(self, start, end):
        # Reset grid and tracking variables
        self.modified_blocks.clear()
        path = []
        visited = set()

        # Perform a DFS to generate path from start to end
        if self.dfs(start, end, visited, path):
            return path
        else:
            return None

    def dfs(self, current, end, visited, path):
        # Base case: If we've reached the end, add the current node to path
        if current == end:
            path.append(current)
            return True

        visited.add(current)
        neighbors = self.get_neighbours(current)
        
        # Explore neighbors only if not visited and ensures uniqueness of the path
        for neighbor in neighbors:
            if neighbor not in visited:
                if self.dfs(neighbor, end, visited, path):
                    path.append(current)
                    return True

        visited.remove(current)
        return False

    def validate_single_path(self, path):
        # Ensure there is no other path from start to end that diverges
        visited = set()
        valid_paths = 0  # Count valid paths

        def dfs(current_pos):
            nonlocal valid_paths
            if current_pos == self.end:
                valid_paths += 1
                if valid_paths > 1:  # Found more than one path
                    return True  # Early stop if more than one path
            visited.add(current_pos)
            for neighbor in self.get_neighbours(current_pos):
                if neighbor not in visited and neighbor in path:  # Only check the path cells
                    if dfs(neighbor):
                        return True
            visited.remove(current_pos)
            return False

        # Start depth-first search from start to end
        dfs(self.start)

        # There should only be one valid path
        return valid_paths == 1

    def get_blocks(self):
        return self.blocks
