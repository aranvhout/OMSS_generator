from enum import Enum, auto

# Define the possible shapes for subshapes
class SubShapes(Enum):
    TRIANGLE = auto()
    SQUARE = auto()
    CIRCLE = auto()
    # Add other shapes if needed

# Define line shapes (whether straight or curved)
class LineShape(Enum):
    STRAIGHT = auto()
    CURVED = auto()

# Subentity class that contains lines and subshapes
class SubEntity:
    def __init__(self, lines=None, subshapes=None):
        self.lines = lines if lines is not None else []
        self.subshapes = subshapes if subshapes is not None else []

    def add_line(self, line):
        self.lines.append(line)

    def add_subshape(self, subshape):
        self.subshapes.append(subshape)

# Lines class with attributes for number, position, and shape
class Line:
    def __init__(self, number, position, shape: LineShape):
        self.number = number  # Number of lines
        self.position = position  # Could be an array of coordinates or description of location
        self.shape = shape  # Shape of the line (straight or curved)

# Subshapes class with attributes for shape, color, and number
class SubShape:
    def __init__(self, shape: SubShapes, color, number):
        self.shape = shape  # Shape of the subshape
        self.color = color  # Color of the subshape (could link to Colors enum)
        self.number = number  # Number of this type of subshape
# Create instances of Line and SubShape
line1 = Line(number=3, position="top-left", shape=LineShape.CURVED)
subshape1 = SubShape(shape=SubShapes.CIRCLE, color="RED", number=5)

# Create a SubEntity and add line and subshape instances to it
sub_entity = SubEntity()
sub_entity.add_line(line1)
sub_entity.add_subshape(subshape1)

print(sub_entity.lines)      # Outputs the list of lines in sub_entity
print(sub_entity.subshapes)   # Outputs the list of subshapes in sub_entity
