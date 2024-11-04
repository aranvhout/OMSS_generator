from enum import Enum, auto

#For the subshape class
class SubShapeShapes(Enum):
    TRIANGLE = auto()
    SQUARE = auto()
    PENTAGON = auto ()
    CIRCLE = auto()
        
class SubShapePosition(Enum):
    TOPLEFT = auto()
    TOPRIGHT = auto()
    BOTTOMLEFT = auto ()
    BOTTOMRIGHT = auto()
 
class SubShapeNumber (Enum):
    SINGLE = auto ()
    DOUBLE = auto ()
    TRIPLE = auto ()
    
class SubShapeColors(Enum): #could also take colours from the entity module, for now I keep it seperaate
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()

class SubShape:
    def __init__(self, shape: SubShapeShapes, color: SubShapeColors, number: SubShapeNumber, position: SubShapePosition):
        self.shape = shape             # Shape of the subshape, using SubShapeShapes enum
        self.color = color             # Color of the subshape, using Colors enum
        self.number = number           # Number of subshapes, using SubShapeNumber enum
        self.position = position       # Position of the subshape, using SubShapePosition enum

    
#For the line class
class LineShape(Enum):
    STRAIGHT = auto()
    CURVED = auto()

class LineNumber (Enum):
    SINGLE = auto ()
    DOUBLE = auto ()
    TRIPLE = auto ()
    
class LineAngles (Enum):
    ZERO = auto()
    FORTYFIVE = auto()
    NINETY = auto()

# Lines class with attributes for number, position, and shape
class Line:
    def __init__(self, number: LineNumber, shape: LineShape, angle = LineAngles):
        self.number = number  # Number of lines
        self.angle = angle  # Could be an array of coordinates or description of location
        self.shape = shape  # Shape of the line (straight or curved)    

# Subentity class that contains lines and subshapes
class SubEntity:
    def __init__(self, lines=None, subshapes=None):
        self.lines = lines if lines is not None else []
        self.subshapes = subshapes if subshapes is not None else []

    def add_line(self, line):
        self.lines.append(line)

    def add_subshape(self, subshape):
        self.subshapes.append(subshape)




