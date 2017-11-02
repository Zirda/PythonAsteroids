from polygon import Polygon
from point import Point
from circle import Circle

class Ship (Polygon):
    def __init__(self):
        self.points = [Point(0, 0), Point(0, 5), Point(-10, 10), Point(15, 0), Point(-10, -10), Point(0, -5)]
        self.position = Point(5,5)
        self.rotation = 0
        self.pull = Point(0.1,0.1)
        self.angular_velocity = 0.0

        # super().__init__(self)



    # TODO: Define a ship