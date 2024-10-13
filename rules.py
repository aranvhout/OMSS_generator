# rules.py

from enum import Enum, auto
from entity import Shapes, Sizes, Colors, Angles, AttributeType, Entity
import random

class Ruletype(Enum):
    RANDOM = auto()
    CONSTANT = auto()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()

# Define the valid shape progression order
progression_shapes = [Shapes.TRIANGLE, Shapes.SQUARE, Shapes.PENTAGON, Shapes.HEXAGON, Shapes.DECAGON, Shapes.CIRCLE]

def get_next_shape(current_shape):#i think i want to move this in the future for clarity reasons
    index = progression_shapes.index(current_shape)
    next_index = (index + 1) % len(progression_shapes)
    return progression_shapes[next_index]

def apply_rule(rule, attribute, entity):
    # Constant
    if rule == Ruletype.CONSTANT:
        if attribute == AttributeType.SHAPE:
            return entity.shape
        elif attribute == AttributeType.SIZE:
            return entity.size
        elif attribute == AttributeType.COLOR:
            return entity.color            
        elif attribute == AttributeType.ANGLE:
            return entity.angle

    # Progression
    if rule == Ruletype.PROGRESSION:
        if attribute == AttributeType.SHAPE:
            #apply constraints 
            return get_next_shape(entity.shape)
        elif attribute == AttributeType.SIZE:
            pass  # Placeholder for size progression rule logic
        elif attribute == AttributeType.COLOR:
            pass  # Placeholder for color progression rule logic
        elif attribute == AttributeType.ANGLE:
            pass  # Placeholder for angle progression rule logic

    # Distribute Three
    if rule == Ruletype.DISTRIBUTE_THREE:
        if attribute == AttributeType.SHAPE:
            pass  # Placeholder for shape distribute three rule logic
        elif attribute == AttributeType.SIZE:
            pass  # Placeholder for size distribute three rule logic
        elif attribute == AttributeType.COLOR:
            pass  # Placeholder for color distribute three rule logic
        elif attribute == AttributeType.ANGLE:
            pass  # Placeholder for angle distribute three rule logic
            
    # Random
    if rule == Ruletype.RANDOM:
        if attribute == AttributeType.SHAPE:
            return random.choice(list(Shapes))
        elif attribute == AttributeType.SIZE:
            return random.choice(list(Sizes))
        elif attribute == AttributeType.COLOR:
            return random.choice(list(Colors))
        elif attribute == AttributeType.ANGLE:
            return Angles.random_angle()

    # Return the unchanged attribute if no rule applies
    if attribute == AttributeType.SHAPE:
        return entity.shape
    elif attribute == AttributeType.SIZE:
        return entity.size
    elif attribute == AttributeType.COLOR:
        return entity.color            
    elif attribute == AttributeType.ANGLE:
        return entity.angle
