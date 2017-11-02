import random
import time
from polygon import Polygon
from point import Point
from circle import Circle

class Ship (Polygon):
    def __init__(self):
        self.points = [Point(0, 0), Point(0, 5), Point(-10, 10), Point(15, 0), Point(-10, -10), Point(0, -5)]
        self.position = Point(640,360)
        self.rotation = 0
        self.pull = Point(0,-0.2)
        self.angular_velocity = 0.0

        # super().__init__(self)

class Asteroid (Polygon):
    def __init__(self):
        self.points = random.choice([[Point(10,30), Point(25,25), Point(33,11), Point(35,-7), Point(21,-13),            # Chooses one of two asteroid-designs for each asteroid
                                      Point(13,-29), Point(-13,-31), Point(-21,-28), Point(-28,-22), Point(-34,-6),
                                      Point(-32,14), Point(-29,21), Point(-15,9), Point(-23,24), Point(-10,30)],
                                     [Point(0,10), Point(10,15), Point(18,9), Point(13,3), Point(17,-5), Point(5,-12),
                                      Point(-10,-12), Point(-16,-7), Point(-16,8), Point(-9,14)]])
        # Large asteroid: [Point(10,30), Point(25,25), Point(33,11), Point(35,-7), Point(21,-13, Point(13,-29), Point(-13,-31), Point(-21,-28), Point(-28,-22), Point(-34,-6), Point(-32,14), Point(-29,21), Point(-15,9), Point(-23,24), Point(-10,30)]
        # Small asteroid: [Point(0,10), Point(10,15), Point(18,9), Point(13,3), Point(17,-5), Point(5,-12), Point(-10,-12), Point(-16,-7), Point(-16,8), Point(-9,14)]
        self.position = Point(random.randrange(0, 1280, 5),random.randrange(0, 720, 5))
        self.rotation = random.randrange(0, 359, 15)
        self.pull = Point(round(random.uniform(-1, 1),1),round(random.uniform(-1, 1),1))
        self.angular_velocity = round(random.uniform(-1, 1),1)

class Bullet (Circle):
    def __init__(self,position, rotation):
        self.position = position
        self.rotation = rotation
        self.pull = Point(0,0)
        self.angular_velocity = 0
        self.radius = 2
        self.linewidth = 2
        self.accelerate(2)

class Star (Circle):
    def __init__(self):
        self.position = Point(random.randrange(0, 1280, 5),random.randrange(0, 720, 5))
        self.rotation = 0
        self.pull = Point(0.0)
        self.angular_velocity = 1
        self.radius = 1
        self.linewidth = 1





# TODO: Classes Bullet(Circle), Star(Circle)

