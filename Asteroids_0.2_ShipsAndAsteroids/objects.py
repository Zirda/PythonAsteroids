import random
from polygon import Polygon
from point import Point
from circle import Circle

class Ship (Polygon):
    def __init__(self):
        self.points = [Point(0, 0), Point(0, 5), Point(-10, 10), Point(15, 0), Point(-10, -10), Point(0, -5)]
        self.position = Point(640,360)
        self.rotation = random.randrange(0, 360, 15)
        self.pull = Point(0,-0.2)
        self.angular_velocity = 0.0

        # super().__init__(self)

class Asteroid (Polygon):
    def __init__(self):
        self.points = [Point(0,10), Point(10,15), Point(18,9), Point(13,3), Point(17,-5), Point(5,-12), Point(-10,-12), Point(-16,-7), Point(-16,8), Point(-9,14)]
        self.position = Point(random.randrange(0, 1280, 5),random.randrange(0, 720, 5))
        self.rotation = random.randrange(0, 359, 15)
        self.pull = Point(round(random.uniform(-1, 1),1),round(random.uniform(-1, 1),1))
        self.angular_velocity = round(random.uniform(-1, 1),1)

class Bullet (Circle):
    pass

class Star (Circle):
    pass




# TODO: Classes Bullet(Circle), Star(Circle)

