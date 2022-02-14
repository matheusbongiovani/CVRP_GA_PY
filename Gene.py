class Gene(object):
    def __init__(self, x=0, y=0, z=0, id=0):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def distance_from_origin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return ((dx ** 2) + (dy ** 2)) ** 0.5

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getId(self):
        return int(self.id)

    def __str__(self):
        return 'id:' + str(self.getId()) + ' (' + str(self.getX()) + ',' + str(self.getY()) + ')' + ' demand:' + str(self.getZ())

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x


# c0 = Node(0, 0)
# c1 = Node(-1, -1)
# c2 = Node(2, 2)
# print(c1.distance(c2))
# print(c1.distance_from_origin())
# print(c1)
# print(c2)
# print(c1 == c2)
