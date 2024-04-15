from dataclasses import dataclass
from typing import Any


"""
The quadTree structure divide the 2-dimensional array to four subarray:
         __________________
        |        |         |
        |        |         |
        |   NW   |   NE    |
        |        |         |
        |--------|---------|
        |        |         |
        |   SW   |   SE    |
        |        |         |
        |________|_________|


"""


@dataclass
class Point:
    x:float
    y:float


@dataclass
class Element:
    pos:Point
    data:Any

@dataclass
class QuadTree:
    upper_right_boundary:Point
    lower_left_boundary:Point
    n: Element = None
    northwest_part = None
    northeast_part = None
    southwest_part=  None
    southeast_part = None


    def in_boundary(self, point:Point) ->bool:
        return (
                self.upper_right_boundary.x <= point.x <= self.lower_left_boundary.x
                and self.upper_right_boundary.y <= point.y <= self.lower_left_boundary.y
        )


    def insert(self, element: Element):
        if not element:
            return
        if not self.in_boundary(element.pos):
            return

        if (
            (self.lower_left_boundary.x-self.upper_right_boundary.x) <= 1
            and (self.lower_left_boundary.y-self.upper_right_boundary.y) <= 1
        ):
            if not self.n:
                self.n = element
            return
        if self.search(element.pos):
            print(f'Position {element.pos.x, element.pos.y} is already occupied')
            return

        if element.pos.x <= (self.upper_right_boundary.x + self.lower_left_boundary.x)/2:
            # NORTHWEST
            if element.pos.y <= (self.upper_right_boundary.y + self.lower_left_boundary.y)/2:
                if not self.northwest_part:
                    self.northwest_part = QuadTree(
                        self.upper_right_boundary,
                        Point(
                            (self.upper_right_boundary.x + self.lower_left_boundary.x)/2,
                            (self.upper_right_boundary.y + self.lower_left_boundary.y)/2)
                    )
                self.northwest_part.insert(element)
            # SOUTHWEST
            else:
                if not self.southwest_part:
                    self.southwest_part = QuadTree(
                        Point(
                            # (self.upper_right_boundary.x + self.lower_left_boundary.x)/2,
                            # self.upper_right_boundary.y
                            self.upper_right_boundary.x,
                            (self.upper_right_boundary.y + self.lower_left_boundary.y) / 2,
                        ),
                        Point(
                            # self.lower_left_boundary.x,
                            # (self.upper_right_boundary.y + self.lower_left_boundary.y)/2
                            (self.upper_right_boundary.x + self.lower_left_boundary.x) / 2,
                            self.lower_left_boundary.y,

                        )
                    )
                self.southwest_part.insert(element)


        else:
            # NORTHEAST
            if element.pos.y <= (self.upper_right_boundary.y + self.lower_left_boundary.y) / 2:
                if not self.northeast_part:
                    self.northeast_part = QuadTree(
                        Point(
                            # self.upper_right_boundary.x,
                            # (self.upper_right_boundary.y + self.lower_left_boundary.y)/2
                            (self.upper_right_boundary.x + self.lower_left_boundary.x) / 2,
                            self.upper_right_boundary.y


                        ),
                        Point(
                            # (self.upper_right_boundary.x + self.lower_left_boundary.x)/2,
                            # self.lower_left_boundary.y
                            self.lower_left_boundary.x,
                            (self.upper_right_boundary.y + self.lower_left_boundary.y) / 2

                        )
                    )

                self.northeast_part.insert(element)

            # SOUTHEAST
            else:

                if not self.southeast_part:
                    self.southeast_part = QuadTree(
                        Point(
                            (self.upper_right_boundary.x + self.lower_left_boundary.x)/2,
                            (self.upper_right_boundary.y + self.lower_left_boundary.y)/2,
                            ),
                        self.lower_left_boundary
                    )
                self.southeast_part.insert(element)

    def search(self, position:Point) -> None | Element:
        if not self.in_boundary(position):
            return None

        if self.n:
            return self.n

        if position.x <= (self.upper_right_boundary.x + self.lower_left_boundary.x)/2:
            # NORTHWEST
            if position.y <= (self.upper_right_boundary.y + self.lower_left_boundary.y)/2:
                if not self.northwest_part:
                   return None
                return self.northwest_part.search(position)
            # SOUTHWEST
            else:
                if not self.southwest_part:
                    return None
                return self.southwest_part.search(position)


        else:
            # NORTHEAST
            if position.y <= (self.upper_right_boundary.y + self.lower_left_boundary.y) / 2:
                if not  self.northeast_part:
                    return None
                return self.northeast_part.search(position)

            # SOUTHEAST
            else:

                if not  self.southeast_part:
                    return None

                return self.southeast_part.search(position)



element1 = Element(Point(5, 5), "elem1")
element2 = Element(Point(0, 0), "elem2")
element3 = Element(Point(7, 5), "elem3")
element4 = Element(Point(7, 5), "elem4")
upper_limit = Point(0,0)
lower_limit = Point(10,10)

qt = QuadTree(upper_limit, lower_limit)
qt.insert(element1)
qt.insert(element2)
qt.insert(element3)
qt.insert(element4)
#print(f'{qt.search(Point(5, 57)).data}')
print(f'{qt.search(Point(5, 5)).data}')
print(f'{qt.search(Point(0, 0)).data}')
print(f'{qt.search(Point(7, 5)).data}')



