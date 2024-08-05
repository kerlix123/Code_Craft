code = """coms = []
class Steve:
    global coms
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def go_up(self, n):
        self.y += n
        coms.append(("up", n))
    def go_down(self, n):
        self.y -= n
        coms.append(("down", n))
    def go_right(self, n):
        self.x += n
        coms.append(("right", n))
    def go_left(self, n):
        self.x -= n
        coms.append(("left", n))

steve = Steve(0, 0)
steve.go_right(5)
for i in range(2):
    steve.go_left(2)
    steve.go_up(2)
steve.go_down(3)"""

from code_runner import exec_code

print(exec_code(code)["vars"]["coms"])