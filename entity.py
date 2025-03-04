from enum import Enum, auto
from seed import random_choice

class Shapes(Enum):
    TRIANGLE = auto()
    SQUARE = auto()
    PENTAGON = auto()
    SEPTAGON = auto()
    DECAGON = auto()
    CIRCLE = auto()

class Sizes(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


class Colors(Enum):
    RED = auto()
    PINK = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    LAVENDER = auto()
    BROWN = auto()
    ORANGE = auto ()#
           
class Angles(Enum):
    ZERO = auto()
    THIRTY_SIX = auto()
    SEVENTY_TWO = auto()
    ONE_HUNDRED_EIGHT = auto()
    ONE_FORTY_FOUR = auto()
    ONE_EIGHTY = auto()
    TWO_SIXTEEN = auto()
    TWO_FIFTY_TWO = auto()
    TWO_EIGHTY_EIGHT = auto()
    THREE_TWENTY_FOUR = auto()

class Positions (Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_LEFT = auto()
       
# Enum for line types
class Linetypes(Enum):
    SOLID = auto()
    DASHED = auto()
    LARGEDASHED = auto()
    
class Linenumbers(Enum):
    ONE = auto ()
    TWO = auto ()
    THREE = auto ()
    
class Linelengths(Enum):
    SHORT = auto()
    MEDIUM = auto()
    LONG = auto()    

# Enum for line widths
class Linewidths(Enum):
    THIN = auto()
    MEDIUM = auto()
    THICK = auto()


# Class for BigShape entity
class BigShape:
    def __init__(self, shape, size, color, angle, position):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle
        self.position = position
        
        
class LittleShape:
    def __init__(self, shape, size, color, angle, position):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle
        self.position = position
       


# Class for Line entity
class Line:
    def __init__(self, linetype, linewidth, position, size, linelength, angle, linenumber):
        self.linetype = linetype
        self.linewidth = linewidth
        self.position = position
        self.linelength = linelength
        self.linenumber = linenumber
        self.size = size 
        self.angle = angle
        

# Function to create a random entity (either BigShape or Line)
def create_random_entity(seed_list, entity_type=['BigShape'], position = None):
    if entity_type == "BigShape":
        # Create random BigShape attributes
        random_shape, seed_list = random_choice(seed_list, list(Shapes)) 
        random_size, seed_list = random_choice(seed_list, list(Sizes))
        random_color, seed_list = random_choice(seed_list, list(Colors))    
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        
        if position == 'random':
            entity_position, seed_list = random_choice(seed_list, list(Positions))
            
        else:
            entity_position = None
        
        return BigShape(shape=random_shape, size=random_size, color=random_color, angle= random_angle, position= entity_position), seed_list

    elif entity_type == "Line":
        # Create random Line attributes
        random_line_type, seed_list = random_choice(seed_list, list(Linetypes))
        random_line_width, seed_list = random_choice(seed_list, list(Linewidths))
        random_length, seed_list = random_choice(seed_list, list(Linelengths))
        random_number, seed_list = random_choice(seed_list, list(Linenumbers))      
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        if position == 'random':
            entity_position, seed_list = random_choice(seed_list, list(Positions))
            
        else:
            entity_position = None
            
        return Line(linetype=random_line_type, linewidth=random_line_width, position= entity_position, size=Sizes.MEDIUM, linelength = random_length, angle=random_angle, linenumber=random_number), seed_list
    
    
    
    elif entity_type == "LittleShape":
        # Create random BigShape attributes
        random_shape, seed_list = random_choice(seed_list, list(Shapes)) 
        random_size, seed_list = random_choice(seed_list, list(Sizes))
        random_color, seed_list = random_choice(seed_list, list(Colors))    
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        
        if position == 'random':
            entity_position, seed_list =random_choice(seed_list, list(Positions))
            
        else:
            entity_position = None
        
        return LittleShape(shape=random_shape, size=random_size, color=random_color, angle=random_angle, position= entity_position), seed_list

    else:
        raise ValueError("Unknown entity type")



   
        