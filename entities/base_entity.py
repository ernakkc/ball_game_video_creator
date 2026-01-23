class BaseEntity:
    def __init__(self, space):
        self.space = space
        self.body = None
        self.shape = None

    def update(self, dt):
        pass
