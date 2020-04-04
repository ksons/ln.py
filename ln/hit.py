class Hit:

    def __init__(self, shape, t):
        self.shape = shape
        self.t = t

    def ok(self) -> bool:
        return self.t < float("inf")

    def min(self, other):
        if self.t <= other.t:
            return self

        return other

    def max(self, other):
        if self.t > other.t:
            return self

        return other


NoHit = Hit(None, float("inf"))
