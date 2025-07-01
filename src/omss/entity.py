#OMSS imports
from .seed import random_choice

#general imports
from enum import Enum, auto
import random

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
    BLUE = auto()
    ORANGE = auto()
    GREEN = auto()
    BROWN = auto()
    PURPLE = auto()
    GRAY = auto()
    RED = auto()
    YELLOW = auto ()#

      
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
       

class Linetypes(Enum):
    SOLID = auto()
    CURVE= auto()
    WAVE = auto()
    
class Linenumbers(Enum):
    ONE = auto ()
    TWO = auto ()
    THREE = auto ()
    FOUR = auto ()
    FIVE = auto ()
    
class Bigshapenumbers(Enum):
    ONE = auto ()
   
class Littleshapenumbers (Enum):
     ONE = auto ()
     TWO = auto ()
     THREE = auto ()
     FOUR = auto ()

# Class for BigShape element
class BigShape:
    def __init__(self, shape, size, position, color, angle, element_index, number):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle        
        self.element_index = element_index
        self.number = number
        self.position = position  
        
        

class LittleShape:
    _seed = None
    _random_instance = None

    @classmethod
    def set_seed(cls, seed):
        if cls._seed is not None:
            raise RuntimeError("Seed has already been set and cannot be changed.")
        cls._seed = seed
        cls._random_instance = random.Random(seed)
        
    @classmethod
    def reset_seed(cls): 
        cls._seed = None
        cls._random_instance = None
    def __init__(self, shape, size, color, angle, position, element_index, littleshapenumber):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle
        self.position = position
        self.element_index = element_index
        self._littleshapenumber = None
        self.littleshapenumber = littleshapenumber  # triggers setter

    @property
    def littleshapenumber(self):
        return self._littleshapenumber

    @littleshapenumber.setter
    def littleshapenumber(self, value):
        if value is None:
            self._littleshapenumber = None
            self.element_index = None
            return

        if not hasattr(value, "name"):
            raise TypeError("littleshapenumber must be a Littleshapenumbers enum")

        name_to_int = {
            "ONE": 1,
            "TWO": 2,
            "THREE": 3,
            "FOUR": 4
        }

        count = name_to_int.get(value.name.upper())
        if count is None:
            raise ValueError(f"Unsupported littleshapenumber: {value.name}")

        self._littleshapenumber = value
        positions_list = sorted(Positions, key=lambda p: p.name)

        # Use seeded randomness if available, otherwise fallback to unseeded
        rnd = LittleShape._random_instance or random
        self.position = rnd.sample(positions_list, count)

        


# Class for Line element
class Line:
    def __init__(self, linetype,  position,  angle, linenumber, element_index):
        self.linetype = linetype        
        self.position = position      
        self.linenumber = linenumber    
        self.angle = angle
        self.element_index = element_index
        

# Function to create a random element (either BigShape or Line)
def create_random_element(seed_list, element_type, element_index,  position = None):
    if element_type == "BigShape":
        # Create random BigShape attributes
        random_shape, seed_list = random_choice(seed_list, list(Shapes)) 
        random_size, seed_list = random_choice(seed_list, list(Sizes))
        random_color, seed_list = random_choice(seed_list, list(Colors))    
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        random_number, seed_list = random_choice(seed_list, list(Bigshapenumbers))
        
        
        
        return BigShape(shape=random_shape, size=random_size, color=random_color, angle= random_angle, element_index =element_index, number = random_number, position =None ), seed_list
        
    elif element_type == "Line":
        # Create random Line attributes
        random_line_type, seed_list = random_choice(seed_list, list(Linetypes))
        random_number, seed_list = random_choice(seed_list, list(Linenumbers))#makes sure we don't create an empty grid as starting point
        random_angle, seed_list = random_choice(seed_list, list(Angles))
       
        if position == 'random':
            element_position, seed_list = random_choice(seed_list, list(Positions))
            
        else:
            element_position = None
            
        return Line(linetype=random_line_type, position= element_position, angle=random_angle, linenumber=random_number, element_index =element_index), seed_list
    
    
    
    elif element_type == "LittleShape":
        # Create random littleshape attributes
        random_shape, seed_list = random_choice(seed_list, list(Shapes)) 
        random_size, seed_list = random_choice(seed_list, list(Sizes))
        random_color, seed_list = random_choice(seed_list, list(Colors))    
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        random_number, seed_list = random_choice(seed_list, list(Littleshapenumbers))
        
        if position == 'random':
            element_position, seed_list =random_choice(seed_list, list(Positions))
            
        else:
            element_position = None
        
        return LittleShape(shape=random_shape, size=random_size, color=random_color, angle=random_angle, position= element_position, element_index = element_index, littleshapenumber = random_number ), seed_list

    else:
        raise ValueError("Unknown element type")



   
        