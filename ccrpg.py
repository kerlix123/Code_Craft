import random
from collections import deque

blocks = [["plus.png" for _ in range(7)] for _ in range(7)]


def is_within_bounds(pos):
    x, y = pos
    return 0 <= x < 7 and 0 <= y < 7


def is_neighbour(a, b):
    ax, ay = a
    bx, by = b
    return max(abs(ax - bx), abs(ay - by)) == 1


def get_neighbours(pos):
    x, y = pos
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return [(x + dx, y + dy) for dx, dy in directions if is_within_bounds((x + dx, y + dy))]


def bfs_path(blocks, start, end, marker="grass_top.png"):
    visited = set()
    queue = deque([(start, [start])])  # Queue holds (current_position, path_taken)
    while queue:
        current, path = queue.popleft()
        if current == end:  # Found the end
            for x, y in path[1:-1]:  # Skip the start and end points
                blocks[6 - y][x] = marker
            return True  # Path successfully created

        for neighbour in get_neighbours(current):
            if neighbour not in visited and neighbour not in path:
                visited.add(neighbour)  # Mark as visited
                queue.append((neighbour, path + [neighbour]))

    return False  # No path found


# Generate points
start = (random.randint(0, 6), random.randint(0, 6))

end = (random.randint(0, 6), random.randint(0, 6))
while is_neighbour(end, start):
    end = (random.randint(0, 6), random.randint(0, 6))

point_1 = (random.randint(0, 6), random.randint(0, 6))
while is_neighbour(point_1, start) or is_neighbour(point_1, end):
    point_1 = (random.randint(0, 6), random.randint(0, 6))

point_2 = (random.randint(0, 6), random.randint(0, 6))
while is_neighbour(point_2, start) or is_neighbour(point_2, end) or point_2 == point_1:
    point_2 = (random.randint(0, 6), random.randint(0, 6))

# Place the points on the grid
blocks[6-start[1]][start[0]] = "sand.png"
blocks[6-end[1]][end[0]] = "oak_trapdoor.png"
blocks[6-point_1[1]][point_1[0]] = "grass_top.png"
blocks[6-point_2[1]][point_2[0]] = "grass_top.png"

# Connect points using BFS
if not bfs_path(blocks, start, point_1):
    print("Failed to create a path from start to point_1")
if not bfs_path(blocks, point_1, point_2):
    print("Failed to create a path from point_1 to point_2")
if not bfs_path(blocks, point_2, end):
    print("Failed to create a path from point_2 to end")

# Print the grid
for el in blocks:
    print(str(el).replace("'", "\"") + ",")
