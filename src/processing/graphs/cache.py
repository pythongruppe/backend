class GraphCache:

    def __init__(self, data):
        self.data = data
        self.factories = dict()
        self.cache = dict()

    def register(self, key, factory):
        self.factories[key] = factory

    def get(self, key):
        if self.cache.get(key, None) is None:
            self.cache[key] = self.factories[key](self.data)

        return self.cache[key]
