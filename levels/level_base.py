class BaseLevel:
    def __init__(self, space):
        self.space = space
        self.obstacles = []

    def build(self):
        raise NotImplementedError
