import struct
import ctypes
import pathlib
import os
import random
import math
import multiprocessing
from PIL import Image, ImageDraw
from Entity import Entity
from Object import Object
from Building import Building
from Point import Point
from Line import Line
from itertools import repeat

SPI_SETDESKWALLPAPER = 20

def get_global_path():
    return str(pathlib.Path().absolute())

def is_64bit_windows():
    """Check if 64 bit Windows OS"""
    return struct.calcsize('P') * 8 == 64

def changeBackground(path):
    """Change background depending on bit size"""
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 3)

filePath = os.path.join(get_global_path(), f'{0}.jpg')
objects = []
imageSize = (4000, 2000)
buildingSeperation = 25


## too slow in bulk
# use bounding boxes and multithreading to speed up
rayLength = 100
NUM_RAYS = 50
def findRayCollisions(position, otherBuildings, a):
    angle = a/1000
    ray = Line(Point(0, 0), Point(math.cos(angle)*rayLength, math.sin(angle)*rayLength))
    bestCollision = None
    for b in otherBuildings:
        buildingShape = b.shape
        for i in range(len(buildingShape)):
            pPoint = buildingShape[i-1]
            cPoint = buildingShape[i]
            
            polyLine = Line(pPoint + b.position - position, cPoint + b.position - position)
            
            canidatePoint = ray.getCollisionWith(polyLine)
            
            if canidatePoint != None:
                if bestCollision == None or canidatePoint.magnatude < bestCollision.magnatude:
                    bestCollision = canidatePoint
    if bestCollision:
        #bestCollision.setMagnatude(max(0, bestCollision.magnatude - 30))
        bestCollision.setMagnatude(bestCollision.magnatude - 30)
        return bestCollision

def addBuilding(position, otherBuildings, canvas):
    pool = multiprocessing.Pool(processes = 12)
    polyPoints = [Point(0, 0)] + [p for p in pool.starmap(findRayCollisions, zip(repeat(position), repeat(otherBuildings), range(0, int((math.pi*2)*1000), int((math.pi)*1000/NUM_RAYS)))) if p != None]
    
    if len(polyPoints) > 2:
        #canvas.ellipse((position.x, position.y, position.x + 10, position.y + 10), fill=(255, 0, 0), outline=(0, 0, 0))
        objects.append(Building(position, tuple(polyPoints), 1))
    else:
        objects.append(Building(position, [Point(0, 0), Point(random.randint(-100, 100), random.randint(-100, 100)), Point(random.randint(-100, 100), random.randint(-100, 100))]))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    for offset in range(3):
        for x in range(10):
            for y in range(10):
                try:
                    os.remove(filePath)
                except FileNotFoundError:
                    pass
                
                im = Image.new('RGB', (imageSize[0], imageSize[1]), (100, 100, 100))
                draw = ImageDraw.Draw(im)
                
                #angleSeperationInner = sectorAngle - (buildingSeperation/innerLength)
                addBuilding(Point((offset*70) + x*210 + 300, (offset*70) + y*210 + 100), objects, draw)
                
                Object.run(objects, draw, imageSize)
                #objects.clear()
                
                im.save(filePath, quality=95, optimize=False)
                
                changeBackground(filePath)