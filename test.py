import signal
class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    raise TimeoutException("Code execution exceeded time limit")
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)
coms = []
class Mob:
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
mob = Mob(0, 0)

i = 0
while i < 6:
    mob.go_up(2)
    mob.go_right(2)