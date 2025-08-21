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
    YELLOW = auto ()
     
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
    CURVED= auto()
    WAVED = auto()
    
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

class BigShape:
    def __init__(self, shape, size, position, color, angle, element_index, number):
        self.shape = shape
        self.size = size 
        self.color = color
        self.angle = angle        
        self.element_index = element_index
        self.number = number
        self.position = position  
        

class Line:
    def __init__(self, linetype,  position,  angle, linenumber, element_index):
        self.linetype = linetype        
        self.position = position      
        self.linenumber = linenumber    
        self.angle = angle
        self.element_index = element_index
        

        
class LittleShape:
#"""this class was superannoying to make since the number of littleshapes is related to the positions they can occupy, all the extended
#code tries to deal with this"""
    _seed = None
    _random_instance = None

    @classmethod
    def set_seed(cls, seed): #set seed since the positions need to be able to be repeated in case of a seed
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
        self._position = position
        self.element_index = element_index
        self._littleshapenumber = None
        self.littleshapenumber = littleshapenumber  # triggers setter

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

        # update littleshapenumber based on the number of positions
        count = len(value) if isinstance(value, (list, tuple)) else 1
        int_to_name = {
            1: "ONE",
            2: "TWO",
            3: "THREE",
            4: "FOUR"
        }
       
        name = int_to_name.get(count)
        if name and self._littleshapenumber is not None:
            enum_type = type(self._littleshapenumber)
            if hasattr(enum_type, name):
                self._littleshapenumber = getattr(enum_type, name)

    @property
    def littleshapenumber(self):
        return self._littleshapenumber

    @littleshapenumber.setter
    def littleshapenumber(self, value):
        
        if value == None or value == 0:
            
            self._littleshapenumber = None
            self.element_index = None
            self._position = None
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

        # create a sorted list of positions
        positions_list = sorted(Positions, key=lambda p: p.name)

        rnd = LittleShape._random_instance or random
        self._position = rnd.sample(positions_list, count)


        
# function to create a random element which forms the basis of all the modifications by the rules
def create_random_element(seed_list, element_type, element_index,  position = None):
    if element_type == "BigShape":
        # create random BigShape attributes
        random_shape, seed_list = random_choice(seed_list, list(Shapes)) 
        random_size, seed_list = random_choice(seed_list, list(Sizes))
        random_color, seed_list = random_choice(seed_list, list(Colors))    
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        random_number, seed_list = random_choice(seed_list, list(Bigshapenumbers))        
        
        
        return BigShape(shape=random_shape, size=random_size, color=random_color, angle= random_angle, element_index =element_index, number = random_number, position =None ), seed_list
        
    elif element_type == "Line":
        # create random Line attributes
        random_line_type, seed_list = random_choice(seed_list, list(Linetypes))
        random_number, seed_list = random_choice(seed_list, list(Linenumbers))
        random_angle, seed_list = random_choice(seed_list, list(Angles))
       
        if position == 'random': #this kind of legacy code and should be ignored, i didnt leave it out beceause it doesnt hurt anything and will be useful if we want to put back in positions rules
            element_position, seed_list = random_choice(seed_list, list(Positions))
            
        else:
            element_position = None
            
        return Line(linetype=random_line_type, position= element_position, angle=random_angle, linenumber=random_number, element_index =element_index), seed_list
    
        
    elif element_type == "LittleShape":
        # create random littleshape attributes
        random_shape, seed_list = random_choice(seed_list, list(Shapes)) 
        random_size, seed_list = random_choice(seed_list, list(Sizes))
        random_color, seed_list = random_choice(seed_list, list(Colors))    
        random_angle, seed_list = random_choice(seed_list, list(Angles))
        random_number, seed_list = random_choice(seed_list, list(Littleshapenumbers))
        
        if position == 'random': #old legacy code, but i dont want to mess with it since the positions messed me up for like 2 weeks
            element_position, seed_list =random_choice(seed_list, list(Positions))
            
        else:
            element_position = None
        
        return LittleShape(shape=random_shape, size=random_size, color=random_color, angle=random_angle, position= element_position, element_index = element_index, littleshapenumber = random_number ), seed_list

    else:
        raise ValueError("Unknown element type")



   
        