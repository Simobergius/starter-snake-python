
class point:
    def __init__(self,x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, point):
            return point(self.x + other.x, self.y + other.y)
        elif isinstance(other, dict):
            if 'x' in other and 'y' in other:
                return point(self.x + other['x'], self.y + other['y'])
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, point):
            return point(self.x - other.x, self.y - other.y)
        elif isinstance(other, dict):
            if 'x' in other and 'y' in other:
                return point(self.x - other['x'], self.y - other['y'])
        return NotImplemented

    def __str__(self):
        return "x: %d, y: %d" % (self.x, self.y)

    def __repr__(self):
        return "point(%d,%d)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, point):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, dict):
            if 'x' in other and 'y' in other:
                return self.x == other['x'] and self.y == other['y']

    def __ne__(self, other):
        if isinstance(other, point):
            return self.x != other.x or self.y != other.y
        elif isinstance(other, dict):
            if 'x' in other and 'y' in other:
                return self.x != other['x'] or self.y != other['y']
        return NotImplemented

    def dist(self):
        return abs(self.x) + abs(self.y)

def topoint(data):
    if isinstance(data, dict):
        if 'x' in data and 'y' in data:
            return point(data['x'], data['y'])
    else:
        return NotImplemented
