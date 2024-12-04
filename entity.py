from enum import Enum, auto
import random
import numpy as np
from seed import update_seedlist, get_random_attribute

class AttributeType(Enum):#probably move this somewhere else, this doesnt really refer to the entity but rather to what needs to be changed
    SHAPE = auto()        #its more of a setting so probably should be moved to main or something
    SIZE = auto()
    COLOR = auto()
    ANGLE = auto()
    LINETYPE = auto ()
    LINEWIDTH = auto ()
    
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


# Enum for line types
class LineTypes(Enum):
    SOLID = auto()
    DASHED = auto()
    DOTTED = auto()

# Enum for line widths
class LineWidths(Enum):
    THIN = auto()
    MEDIUM = auto()
    THICK = auto()

# Class for BigShape entity
class BigShape:
    def __init__(self, shape, size, color, angle, index=None):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle
        self.index = index 

# Class for Line entity
class Line:
    def __init__(self, linetype, linewidth, color, index=None):
        self.linetype = linetype
        self.linewidth = linewidth
        self.color = color
        self.index = index

# Function to create a random entity (either BigShape or Line)
def create_random_entity(seed_list, entity_type="big-shape"):
    if entity_type == "big-shape":
        # Create random BigShape attributes
        random_shape, seed_list = get_random_attribute(seed_list, list(Shapes)) 
        random_size, seed_list = get_random_attribute(seed_list, list(Sizes))
        random_color, seed_list = get_random_attribute(seed_list, list(Colors))    
        random_angle, seed_list = get_random_attribute(seed_list, list(Angles))
        return BigShape(shape=random_shape, size=random_size, color=random_color, angle=random_angle), seed_list

    elif entity_type == "line":
        # Create random Line attributes
        random_line_type, seed_list = get_random_attribute(seed_list, list(LineTypes))
        random_line_width, seed_list = get_random_attribute(seed_list, list(LineWidths))
        random_color, seed_list = get_random_attribute(seed_list, list(Colors))
        return Line(linetype=random_line_type, linewidth=random_line_width, color=random_color), seed_list

    else:
        raise ValueError("Unknown entity type")



   
        