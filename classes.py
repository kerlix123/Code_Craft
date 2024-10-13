class Level:
    def __init__(self, x, y, level, size, text_closed, levels):
        self.x = x
        self.y = y
        self.level = level
        self.size = size
        self.unlocked = level <= levels["last_finished_level"]+1
        self.text_closed = text_closed
        self.text_page = 0
    def hover(self, x2, y2):
        return self.x <= x2 <= self.x + self.size and self.y <= y2 <= self.y + self.size

class Skin:
    def __init__(self, name, x, y, price, unlocked):
        self.name = name
        self.x = x
        self.y = y
        self.price = price
        self.size = 80
        self.unlocked = unlocked
    def hover(self, x2, y2):
        return self.x <= x2 <= self.x + self.size and self.y <= y2 <= self.y + self.size