from enum import Enum, auto
import random
import numpy as np

class AttributeType(Enum):#probably move this somewhere else, this doesnt really refer to the entity but rather to what needs to be changed
    SHAPE = auto()        #its more of a setting so probably should be moved to main or something
    SIZE = auto()
    COLOR = auto()
    ANGLE = auto()
    
class Attribute:

    def __init__(self, name: AttributeType, values):
        self.name = name
        self.values = np.array(values, dtype="object")


class Shapes(Enum):
    TRIANGLE = auto()
    SQUARE = auto()
    PENTAGON = auto()
    HEXAGON = auto()
    DECAGON = auto()
    CIRCLE = auto()

class Sizes(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

class Colors(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto ()
    PURPLE = auto ()
    

class Angles:
    angles = [0, 20, 40, 60, 80, 100, 120, 140, 160]
    
    @classmethod
    def random_angle(cls):
       return random.choice(cls.angles)

class Entity:
    def __init__(self, shape, size, color, angle,index=None):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle
        self.index = index 

def create_random_entity():
    random_shape = random.choice(list(Shapes))
    random_size = random.choice(list(Sizes))
    random_color = random.choice(list(Colors))
    random_angle = Angles.random_angle() 

    return Entity(shape=random_shape, size=random_size, color=random_color, angle=random_angle)
   
        