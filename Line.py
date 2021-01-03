from Point import Point

class Line:
    def __init__(self, p1, p2):
        self._start = p1
        self._end = p2
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    def getCollisionWith(self, otherLine):
        # calculate the distance to intersection point
        try:
            uA = ((otherLine._end.x-otherLine._start.x)*(self._start.y-otherLine._start.y) - (otherLine._end.y-otherLine._start.y)*(self._start.x-otherLine._start.x)) / ((otherLine._end.y-otherLine._start.y)*(self._end.x-self._start.x) - (otherLine._end.x-otherLine._start.x)*(self._end.y-self._start.y))
            uB = ((self._end.x-self._start.x)*(self._start.y-otherLine._start.y) - (self._end.y-self._start.y)*(self._start.x-otherLine._start.x)) / ((otherLine._end.y-otherLine._start.y)*(self._end.x-self._start.x) - (otherLine._end.x-otherLine._start.x)*(self._end.y-self._start.y))
            
            # if uA and uB are between 0-1, lines are colliding
            if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
                
                # optionally, draw a circle where the lines meet
                intersectionX = self._start.x + (uA * (self._end.x-self._start.x))
                intersectionY = self._start.y + (uA * (self._end.y-self._start.y))
                
                return Point(intersectionX, intersectionY)
        except ZeroDivisionError:
            pass
        return None


## test: (expected: (20, 0)
#l1 = Line(Point(0,0),Point(1000, 0))
#l2 = Line(Point(0, -20), Point(10, -1))
#print(str(l1.getCollisionWith(l2)))