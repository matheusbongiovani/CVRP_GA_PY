import math


class Node(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def distance_from_origin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return math.hypot(dx, dy)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def __str__(self):
        return '<' + str(self.getX()) + ',' + str(self.getY()) + ',' + str(self.getZ()) + '>'

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x


# c1 = Node(2, 2)
# c2 = Node(1, 1)
# print(c1)
# print(c2)
# print(c1 == c2)

# print(c1.distance(c2))
# print(c1.distance_from_origin())
