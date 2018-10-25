
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

    def rotateCCW(self):
        #left (-1, 0)   -> down (0, 1)
        #up (0, -1)     -> left (-1, 0)
        #right (1, 0)   -> up (0, -1)
        #down (0, 1)    -> right (1, 0)
        return point(self.y, -self.x)

    def rotateCW(self):
        #left (-1, 0)   -> up (0, -1)
        #up (0, -1)     -> right (1, 0)
        #right (1, 0)   -> down (0, 1)
        #down (0, 1)    -> left (-1, 0)
        return point(-self.y, self.x)

    def todir(self):
        if self.x == 0 and self.y > 0:
            return 'down'
        elif self.x == 0 and self.y < 0:
            return 'up'
        elif self.x < 0 and self.y == 0:
            return 'left'
        elif self.x > 0 and self.y == 0:
            return 'right'
        else:
            return ''

def topoint(data):
    if isinstance(data, dict):
        if 'x' in data and 'y' in data:
            return point(data['x'], data['y'])
    elif isinstance(data, str):
        if data == 'left':
            return point(-1,0)
        elif data == 'up':
            return point(0,-1)
        elif data == 'down':
            return point(0,1)
        elif data == 'right':
            return point(1,0)
        else:
            return NotImplemented
    else:
        return NotImplemented