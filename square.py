class Square:
    def __init__(self, y, x):
        self.char = None 
        self.y = y
        self.x = x
        self.is_mine = False
        self.marked_mine = False
        self.marked_not_mine = False
        self.visited = False
