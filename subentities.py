from enum import Enum, auto
from seed import get_random_attribute

#rules module for subentities
class SubEntityRuletype(Enum):
    CONSTANT = auto()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()
    
    

# Define enums for types of SubEntities
class SubEntityType(Enum):
    LINE = auto()
    SUBSHAPE = auto()

# Enums for SubShape attributes
class SubShapeShapes(Enum):
    TRIANGLE = auto()
    SQUARE = auto()
    PENTAGON = auto()
    CIRCLE = auto()

class SubShapePosition(Enum):
    TOPLEFT = auto()
    TOPRIGHT = auto()
    BOTTOMLEFT = auto()
    BOTTOMRIGHT = auto()

class SubShapeNumber(Enum):
    SINGLE = auto()
    DOUBLE = auto()
    TRIPLE = auto()

class SubShapeColors(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()

# SubShape class
class SubShape:
    Shapes = SubShapeShapes  
    Colors = SubShapeColors   
    Positions = SubShapePosition
    Numbers = SubShapeNumber
    
    def __init__(self, shape: Shapes, color: Colors, number: Numbers, position: Positions):
        self.shape = shape             
        self.color = color             
        self.number = number           
        self.position = position 
        
# Enums for Line attributes
class LineShapes(Enum):
    STRAIGHT = auto()
    CURVED = auto()

class LineNumbers(Enum):
    SINGLE = auto()
    DOUBLE = auto()
    TRIPLE = auto()

class LineAngles(Enum):
    ZERO = auto()
    FORTYFIVE = auto()
    NINETY = auto()

# Line class
class Line:
    Shapes = LineShapes  # Expose the enum
    Numbers = LineNumbers # Expose the enum
    Angles = LineAngles   # Expose the enum

    def __init__(self, number: Numbers, shape: Shapes, angle: Angles):
        self.number = number  
        self.angle = angle  
        self.shape = shape       


# Factory function to create a SubEntity based on type
def create_random_subentity(subentitytype, seed_list):
        
    if subentitytype == SubEntityType.LINE:
        # Randomly select attributes for a Line
        lineshape, seed_list = get_random_attribute(seed_list, list(LineShapes))
        linenumber, seed_list = get_random_attribute(seed_list, list(LineNumbers))
        lineangle, seed_list = get_random_attribute(seed_list, list(LineAngles))
        
        # Create a Line instance 
        line = Line(number=linenumber, shape=lineshape, angle=lineangle)
        return line
        
    elif subentitytype == SubEntityType.SUBSHAPE:
        # Randomly select attributes for a SubShape
        shape, seed_list = get_random_attribute(seed_list, list(SubShapeShapes))
        color, seed_list = get_random_attribute(seed_list, list(SubShapeColors))
        number, seed_list = get_random_attribute(seed_list, list(SubShapeNumber))
        position, seed_list = get_random_attribute(seed_list, list(SubShapePosition))
        
        # Create a SubShape instance 
        subshape = SubShape(shape=shape, color=color, number=number, position=position)
        return subshape

# Assuming seed_list and create_subentity function are already defined
seed_list = [1444,12,1,999,5,6,7,8,11]


def create_subentity_matrix(n_rows=3, n_columns=3, subentity_rules, seed_list=None):
    subentity_matrix = []
    
    # Extract the class name from the second part of the first rule
    # Assuming the rules are structured correctly
    rule_class_name = subentity_rules[0][1].__class__.__name__  # Gets the class name
    subentity_type = SubEntityType[rule_class_name.upper()]  # Capitalize and map to SubEntityType

    for i in range(n_rows):
        row = []
        for j in range(n_columns):
            # Directly create the subentity using the inferred type
            subentity, seed_list = create_random_subentity(subentity_type, seed_list)
            row.append(subentity)
        subentity_matrix.append(row)

    return subentity_matrix




