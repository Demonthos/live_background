from Object import Object
from Point import Point
import math

class Building(Object):
    SHADOW_SHIFT_PER_HIGHT = (20, 20)
    def __init__(self, position, polygon = [Point(0, 0), Point(50, 0), Point(50, 50), Point(0, 50)], height = 1, fill = (255, 0, 0), outline = (0, 0, 0)):
        super().__init__(position)
        self.shape = tuple(Point(p.x, p.y) for p in polygon)
        self.fill = fill
        self.outline = outline
        self.setHeight(height)
    
    def setHeight(self, height):
        self.height = height
        self.shadowShift = (Building.SHADOW_SHIFT_PER_HIGHT[0] * height, Building.SHADOW_SHIFT_PER_HIGHT[1] * height)
    
    def getShape(self):
        return self.shape
    
    def draw(self, canvas):
        self.drawMain(canvas)
    
    def drawBackground(self, canvas):
        self.drawWalls(canvas)
    
    def drawMain(self, canvas):
        # draw top
        canvas.polygon(tuple((p + self.position).tuple for p in self.shape), self.fill, self.outline)
    
    def drawWalls(self, canvas):
        def shifted(pt):
            return Point(pt.x + self.shadowShift[0], pt.y + self.shadowShift[1])
        
        # draw walls
        darkenedFill = tuple(max(c - 100, 0) for c in self.fill)
        for pIndex in range(len(self.shape)):
            wallShape = []
            
            previousPointIndex = pIndex - 1
            previousPoint = self.shape[previousPointIndex]
            
            currentPoint = self.shape[pIndex]
            
            nextPointIndex = pIndex + 1
            if nextPointIndex >= len(self.shape):
                nextPointIndex = 0
            nextPoint = self.shape[nextPointIndex]
            
            wallShape.append(currentPoint)
            wallShape.append(shifted(currentPoint))
            wallShape.append(shifted(previousPoint))
            wallShape.append(previousPoint)
            
            canvas.polygon(tuple((p + self.position).tuple for p in wallShape), darkenedFill, None)
        
        for currentPoint in self.shape:
            canvas.line((currentPoint + shifted(currentPoint) + self.position).tuple, fill = self.outline, width = 1)