from Object import Object
import math

class Entity(Object):
    def __init__(self, position, volX = 0, volY = 0, looping = True, fill = (255, 0, 0), outline=(0, 0, 0)):
        super().__init__(position)
        self.volX = volX
        self.volY = volY
        self.looping = looping
        self.fill = fill
        self.outline = outline
    
    def draw(self, canvas):
        canvas.ellipse((self.x, self.y, self.x + 10, self.y + 10), self.fill, self.outline)
    
    def process(self, size):
        self.position += position(self.volX, self.volY)
        if self.looping:
            if size[0] == -1 and size[1] == -1:
                raise ValueError('canvas size not passed')
            if self.position.x > size[0]:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = size[0]
            if self.position.y > size[1]:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = size[1]    