from enum import Enum, auto
import random
import numpy as np
from seed import update_seedlist, get_random_attribute

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
    

class Angles(Enum):
    ZERO = auto()
    TWENTY = auto()
    FORTY = auto()
    SIXTY = auto()
    EIGHTY = auto()
    HUNDRED = auto()
    ONE_TWENTY = auto()
    ONE_FORTY = auto()
    ONE_SIXTY = auto()

class Entity:
    def __init__(self, shape, size, color, angle,index=None):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle
        self.index = index 

def create_random_entity(seed_list):
    random_shape = get_random_attribute(seed_list, list(Shapes))
    random_size = get_random_attribute(seed_list, list(Sizes))
    random_color = get_random_attribute(seed_list, list(Colors))
    random_angle = get_random_attribute(seed_list, list(Angles))

    return Entity(shape=random_shape, size=random_size, color=random_color, angle=random_angle)


   
        