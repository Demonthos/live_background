import math

class Object:
    def __init__(self, position):
        self.position = position
    
    def draw(self, canvas):
        raise NotImplementedError
    
    def drawBackground(self, canvas):
        pass
    
    def process(self, size = (-1, -1)):
        pass
    
    @staticmethod
    def run(objects, canvas, size = (-1, -1)):
        generators = []
        for obj in objects:
            obj.process(size)
        
        for obj in objects:
            obj.drawBackground(canvas)
        
        for obj in objects:
            obj.draw(canvas)
    
    def getDistenceTo(self, otherObj):
        return math.sqrt((self.position.x - otherObj.x)**2 + (self.position.y - otherObj.y)**2)