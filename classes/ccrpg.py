import random
class RandomPathGenerator:
    def __init__(self, path_block):
        self.size = 7
        self.blocks = [["plus.png" for _ in range(7)] for _ in range(7)]
        self.start = []
        self.curr = []
        self.path_block = path_block
        self.directions = ["up", "down", "right", "left"]
    
    def is_within_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size
    
    def generate_path(self):
        d = {"up":[], "down":[], "right":[], "left":[]}
        for _ in range(10000):
            direction = random.choice(self.directions)
            if direction == "up":
                if self.curr[0] not in d["up"] and self.curr[0] not in d["down"]:
                    n = random.randint(0, self.size - self.curr[1] - 1)
                    print(n)
                    print()
                    for i in range(n):
                        self.curr[1] += 1
                        self.blocks[6 - self.curr[1]][self.curr[0]] = self.path_block
                    d["up"].append(self.curr[0])
            elif direction == "down":
                if self.curr[0] not in d["up"] and self.curr[0] not in d["down"]:
                    n = random.randint(0, self.curr[1])
                    print(n)
                    print()
                    for i in range(n):
                        self.curr[1] -= 1
                        self.blocks[6 - self.curr[1]][self.curr[0]] = self.path_block
                    d["down"].append(self.curr[0])
            elif direction == "right":
                if self.curr[1] not in d["right"] and self.curr[1] not in d["left"]:
                    n = random.randint(0, self.size - self.curr[0] - 1)
                    print(n)
                    print()
                    for i in range(n):
                        self.curr[0] += 1
                        self.blocks[6 - self.curr[1]][self.curr[0]] = self.path_block
                    d["right"].append(self.curr[1])
            elif direction == "left":
                if self.curr[1] not in d["right"] and self.curr[1] not in d["left"]:
                    n = random.randint(0, self.curr[0])
                    print(n)
                    print()
                    for i in range(n):
                        self.curr[0] -= 1
                        self.blocks[6 - self.curr[1]][self.curr[0]] = self.path_block
                    d["left"].append(self.curr[1])

        self.blocks[6 - self.curr[1]][self.curr[0]] = "oak_trapdoor.png"


    def generate_points(self):
        self.start = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
        self.curr = self.start.copy()
        print(self.start)

        # Place the points on the grid
        self.blocks[6 - self.start[1]][self.start[0]] = self.path_block
    def get_start(self):
        return self.start
    def get_blocks(self):
        return self.blocks