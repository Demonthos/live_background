import struct
import ctypes
import pathlib
import os
import random
import math
from PIL import Image, ImageDraw
from Entity import Entity
from Object import Object
from Building import Building
from Point import Point
from Line import Line
from win32api import GetSystemMetrics

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
imageSize = (GetSystemMetrics(0)*3, GetSystemMetrics(1)*3)
sectorSize = 60
ringSeperation = 25
ringSize = 60
buildingSeperation = 25

def addBuilding(angle, distFromCenter, sectorAngle, buildingSize = 1):
    innerLength = max(distFromCenter - ringSize, 0)
    angleSeperationOuter = (sectorAngle - (buildingSeperation/distFromCenter)) * buildingSize
    angleSeperationInner = angleSeperationOuter
    poly = [
        Point(innerLength*math.cos(angle), innerLength*math.sin(angle)),
        Point(distFromCenter*math.cos(angle), distFromCenter*math.sin(angle)),
        Point(distFromCenter*math.cos(angle + angleSeperationOuter), distFromCenter*math.sin(angle + angleSeperationOuter)),
        Point(innerLength*math.cos(angle + angleSeperationInner), innerLength*math.sin(angle + angleSeperationInner))
        ]
    pointsOutOfFrame = 0
    for p in poly:
        pM = p + Point(imageSize[0]/2, imageSize[1]/2)
        if not (pM.x > 0 and pM.x < imageSize[0] and pM.y > 0 and pM.y < imageSize[1]):
                pointsOutOfFrame += 1
    if pointsOutOfFrame < len(poly):
        objects.append(Building(Point(imageSize[0]/2, imageSize[1]/2), poly, 1, fill=(random.randint(50, 255), 0, random.randint(50, 255))))

for x in range(100):
    distFromCenter = x*(ringSize + ringSeperation)
    sectorDivisions = int((2*math.pi*distFromCenter)/(sectorSize + buildingSeperation))
    if sectorDivisions > 0: sectorAngle = math.pi*2/sectorDivisions
    y = 0
    while y < sectorDivisions:
        buildingSize = random.randint(1, 2)
        
        try:
            os.remove(filePath)
        except FileNotFoundError:
            pass
        
        pLength = len(objects)
        
        angle = y*sectorAngle
        innerLength = max(distFromCenter - ringSize, 0)
        #angleSeperationInner = sectorAngle - (buildingSeperation/innerLength)
        addBuilding(angle, distFromCenter, sectorAngle, 1)
        
        if pLength < len(objects):
            im = Image.new('RGB', (imageSize[0], imageSize[1]), (100, 100, 100))
            draw = ImageDraw.Draw(im)
            
            Object.run(objects, draw, imageSize)
            
            im.save(filePath, quality=95, optimize=False)
            
            changeBackground(filePath)
        
        y += buildingSize

#im = Image.new('RGB', (imageSize[0], imageSize[1]), (100, 100, 100))
#draw = ImageDraw.Draw(im)

#Object.run(objects, draw, imageSize)

#im.save(filePath, quality=95, optimize=False)

#changeBackground(filePath)