from enum import Enum, auto
from entity import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linelengths, Linewidths, AttributeType
from seed import get_random_attribute, update_seedlist

class Ruletype(Enum):
    RANDOM = auto()
    CONSTANT = auto()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()

def apply_rules(matrix, rules, seed_list):
    for rule, attribute in rules:
        if rule == Ruletype.CONSTANT:
            constant_rule(matrix, attribute)
        elif rule == Ruletype.RANDOM:            
            pass  
        elif rule == Ruletype.PROGRESSION:
            progression_rule(matrix, attribute, seed_list)
            seed_list=update_seedlist(seed_list)#we have to update it each time we use this function
        elif rule == Ruletype.DISTRIBUTE_THREE:
            distribute_three(matrix, attribute, seed_list)
            seed_list=update_seedlist(seed_list)#we have to update it each time we use this function
           
            
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
    """Determines the max steps, step size, and direction for a given attribute type to make the progression rule work."""
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
        print(enum_member)
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


       
def distribute_three (matrix, attribute, seed_list):
    # get three unique values from the attribute
    max_value = len(globals()[attribute.name.capitalize() + "s"])
    
    potential_values = list(range(1, max_value + 1))
    distribute_three_values, seed_list = get_random_attribute(seed_list, potential_values, number = 3)
       
        # Assign these values to each entity in the row
    for row in matrix:
        # Create a new randomized order for each row (not the most straightforward way, but I want to update the seed_list)
        
       row_values, seed_list = get_random_attribute(seed_list, distribute_three_values, number = 3)
       
       for i, entity in enumerate(row):
            # Use the shuffled order to assign each value
            value_to_assign = row_values[i]
            
            # Find the corresponding enum member and set it on the entity's attribute
            for enum_member in globals()[attribute.name.capitalize() + "s"]:
                if enum_member.value == value_to_assign:
                    setattr(entity, attribute.name.lower(), enum_member)
                    break
            else:
                raise ValueError(f"No matching enum value found for {value_to_assign}.")
            
  