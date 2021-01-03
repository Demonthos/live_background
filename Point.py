import math

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def __add__(self, p2):
        return Point(self._x + p2._x, self._y + p2._y)
    
    def __sub__(self, p2):
        return Point(self._x - p2._x, self._y - p2._y)        
    
    def __str__(self):
        return f'x: {self._x}, y: {self._y}'
    
    def setMagnatude(self, newMag):
        #raise NotImplementedError
        angle = math.atan(self._y/self._x)
        self._x = math.copysign(math.cos(angle)*newMag, self._x)
        self._y = math.copysign(math.sin(angle)*newMag, self._y)
    
    @property
    def magnatude(self):
        return math.sqrt((self._x**2) + (self._y**2))
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def tuple(self):
        return (self._x, self._y)