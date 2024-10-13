
from entity import Shapes, Sizes, Colors, Angles, AttributeType, Entity
from rules import Ruletype, progression_shapes


# Example constraint functions
def shape_progression_constraint(entity, rule):
    if rule == Ruletype.PROGRESSION:
        entity.shape = progression_shapes[0]#hardcoded to zero for now, but could really take any shape
        
    return entity

def size_constraint(entity, rule):
    # Define specific constraints for size if needed
    return entity

def color_constraint(entity, rule):
    # Define specific constraints for color if needed
    return entity

def angle_constraint(entity, rule):
    # Define specific constraints for angle if needed
    return entity

# Function to apply constraints
def apply_constraints(entity, rules):
    for rule, attribute in rules:
        if attribute == AttributeType.SHAPE:
           
            entity = shape_progression_constraint(entity, rule)
        elif attribute == AttributeType.SIZE:
            entity = size_constraint(entity, rule)
        elif attribute == AttributeType.COLOR:
            entity = color_constraint(entity, rule)
        elif attribute == AttributeType.ANGLE:
            entity = angle_constraint(entity, rule)
    return entity
