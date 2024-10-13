# row.py

from entity import create_random_entity, Entity
from rules import apply_rule, Ruletype, AttributeType
from constraints import apply_constraints

def create_row(rules):
    # Generate the first item randomly
    first_entity = create_random_entity()

    # Apply constraints to the first entity
    first_entity = apply_constraints(first_entity, rules)
    first_entity.index = 0 

    # Store entities in a list for further modifications
    row_entities = [first_entity]
    
    # Generate the next items by applying the specified rules iteratively
    current_entity = first_entity
    for i in range(2):  # Adjusted to generate 3 entities in total (index 0, 1, 2)
        new_shape = current_entity.shape
        new_size = current_entity.size
        new_color = current_entity.color
        new_angle = current_entity.angle
        
        for rule, attribute in rules:
            if attribute == AttributeType.SHAPE:
                new_shape = apply_rule(rule, AttributeType.SHAPE, current_entity)
            elif attribute == AttributeType.SIZE:
                new_size = apply_rule(rule, AttributeType.SIZE, current_entity)
            elif attribute == AttributeType.COLOR:
                new_color = apply_rule(rule, AttributeType.COLOR, current_entity)
            elif attribute == AttributeType.ANGLE:
                new_angle = apply_rule(rule, AttributeType.ANGLE, current_entity)
        
        new_entity = Entity(shape=new_shape, size=new_size, color=new_color, angle=new_angle, index=i+1)
        #new_entity = apply_constraints(new_entity, r
        row_entities.append(new_entity)
        current_entity = new_entity
    
    return row_entities
