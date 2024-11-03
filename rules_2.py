#MATRIX
from entity import create_random_entity, Entity
from seed import update_seedlist, get_random_attribute
import random 

vector = [0,1,2,3,4,5,6,7,8,9]
random.seed(None)
seed_list=random.choices(vector, k=15)
#print(seed_list)
#seed_list=[9,5,4,3,10]

#seed_list=[9,8,10]
def create_starting_matrix(n_rows=3, n_columns=3, seed_list=None, z=None):
    if z is not None:  # 3D matrix case
        matrix = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                depth = []
                for k in range(z):
                    depth.append(create_random_entity(seed_list))
                row.append(depth)
            matrix.append(row)
            
    else:  # 2D matrix case
        matrix = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                entity, seed_list = create_random_entity(seed_list)
                row.append(entity)
            matrix.append(row)
    
    return matrix

matrix=create_starting_matrix(3,3,seed_list)

a =  False
if a is True:
    for row_index, row in enumerate(matrix):
        print(f"\nRow {row_index + 1}:")
        for i, entity in enumerate(row):
            print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")

#rules2


from enum import Enum, auto
from entity import Shapes, Sizes, Colors, Angles, AttributeType, Entity


class Ruletype(Enum):
    RANDOM = auto()
    CONSTANT = auto()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()
    
#main module
rules = [
    (Ruletype.PROGRESSION, AttributeType.SHAPE),
    (Ruletype.PROGRESSION, AttributeType.SIZE),
    (Ruletype.PROGRESSION, AttributeType.COLOR),
    (Ruletype.PROGRESSION, AttributeType.ANGLE)
]

def apply_rules(matrix, rules, seed_list = None ):
    for rule, attribute in rules:
        if rule == Ruletype.CONSTANT:
            constant_rule(matrix, attribute)
        elif rule == Ruletype.RANDOM:            
            pass  
        elif rule == Ruletype.PROGRESSION:
            progression_rule(matrix, attribute, seed_list)
        elif rule == Ruletype.DISTRIBUTE_THREE:
            distribute_three(matrix, attribute, seed_list)
            
            
            
    return matrix

#CONSTANT            
def constant_rule(matrix, attribute):
    for row in matrix:
        # Get the attribute value of the first entity in the row
        constant_value = getattr(row[0], attribute.name.lower())
        # Set this constant value for the specified attribute across all entities in the row
        for entity in row:
            setattr(entity, attribute.name.lower(), constant_value)
            
#PROGRESSION            
def determine_progression_params(attribute, seed_list):
    """Determines the max steps, step size, and direction for a given attribute type."""
    max_value = len(globals()[attribute.name.capitalize() + "s"])#this line works, chatgpt came up with it, i dont fully understand the globals part
    possible_step_sizes = [1]#stepsize 1 is always possible, I iniatialise it already here, so that it will occur twice in the stepsize list, giving it more chance to occur
  
    #add 2 to potenrial stepsizes if possible
    for step_size in [1, 2]:
      if max_value / step_size >= 2:
          possible_step_sizes.append(step_size)
          
          
    # based on seed chose step_size and direction 
       
    step_size, seed_list = get_random_attribute(seed_list, possible_step_sizes)
    direction, seed_list = get_random_attribute(seed_list, [-1,1])
    
    return max_value, step_size, direction

def adjust_starting_entity(entity, attribute, max_value, step_size, direction):
    """Adjust the starting entity's attribute value to ensure a valid progression is possible."""
    current_value = getattr(entity, attribute.name.lower()).value
    
    # Calculate potential ending value after progression
    potential_value = current_value + (step_size * 2 * direction)
    
    # Adjust for upward direction
    if direction == 1:  # Upward progression
        if potential_value > max_value:  # If it exceeds max value
            # Reduce current value just enough
            current_value = max_value - (step_size * 2)
            
    
    # Adjust for downward direction
    elif direction == -1:  # Downward progression
        if potential_value < 1:  # If it goes below 1 (enum starts at 1)
            # Increase current value just enough
            current_value = (step_size * 2) + 1  # Set to the lowest valid value *fun fact python indexing screwed me over so took me hours to find this 
            
    
    # Set the adjusted current value back to the entity
    for enum_member in globals()[attribute.name.capitalize() + "s"]:
     if enum_member.value == current_value:
         #print(enum_member, current_value, step_size, potential_value)
         setattr(entity, attribute.name.lower(), enum_member)     
         break
    else:
       raise ValueError(f"No matching enum value found for {current_value}.")
     
def progression_rule(matrix, attribute, seed_list):
    """Applies a progression rule across each row for a given attribute."""
    
    # Get the maximum value, step size, and direction for the progression
    max_value, step_size, direction = determine_progression_params(attribute, seed_list)
    
    for row in matrix:
        # Adjust the starting entity's attribute to ensure valid progression
        current_value = getattr(row[0], attribute.name.lower()).value
        
        
        adjust_starting_entity(row[0], attribute, max_value, step_size, direction)

        # Get the starting value and apply progression across the row
        current_value = getattr(row[0], attribute.name.lower()).value
       
        for i, entity in enumerate(row):
            # Calculate the new value using the progression formula
            new_value = (current_value + i * step_size * direction) 
           
            # Set the new value to the entity, using the corresponding enum
            for enum_member in globals()[attribute.name.capitalize() + "s"]:
                if enum_member.value == new_value:
                    setattr(entity, attribute.name.lower(), enum_member)
                    break
            else:                    
                raise ValueError(f"No matching enum value found for {new_value}.", attribute)


       
def distribute_three (matrix, attribute, seed_list)  

            
new_matrix=apply_rules(matrix, rules, seed_list)



a =  True
if a is True:
    for row_index, row in enumerate(new_matrix):
        print(f"\nRow {row_index + 1}:")
        for i, entity in enumerate(row):
            print(f"  Entity {i + 1}: Shape={entity.shape.value}, Size={entity.size.value}, Color={entity.color.value}, Angle={entity.angle.value}")
            
            
            
            
