from enum import Enum, auto
from typing import Optional
from entity import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linelengths, Linewidths, AttributeType, Linenumbers
from seed import get_random_attribute, update_seedlist, random_shuffle
import numpy as np

ATTRIBUTE_TO_ENUM = {
    AttributeType.COLOR: Colors,
    AttributeType.SHAPE: Shapes,
    AttributeType.SIZE: Sizes,
    AttributeType.ANGLE: Angles,
    AttributeType.POSITION: Positions,
    AttributeType.LINETYPE: Linetypes,
    AttributeType.LINEWIDTH: Linewidths,
    AttributeType.LINELENGTH: Linelengths,
    AttributeType.LINENUMBER: Linenumbers,
}

class Ruletype(Enum):
    RANDOM = auto()
    CONSTANT = auto()
    FULL_CONSTANT = auto ()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()
    
    
class Rule:
    def __init__(self, rule_type: Ruletype, attribute, value: Optional[str] = None):
        self.rule_type = rule_type
        self.attribute = attribute
        self.value = value  # Optional additional value    
  
def apply_rules(matrix, rules, seed_list):
    binding_list = [] #for now this is only relevant for dist3, basically it check
    for rule_obj in rules:
        rule = rule_obj.rule_type  # Accessing rule_type from Rule object
        attribute = rule_obj.attribute
        value = rule_obj.value  # Optional additional value
        
        
        if rule == Ruletype.CONSTANT:
            constant_rule(matrix, attribute)
            
        elif rule == Ruletype.FULL_CONSTANT:
            full_constant_rule(matrix, attribute, value)
                        
        elif rule == Ruletype.RANDOM:            
            pass  
        
        elif rule == Ruletype.PROGRESSION:
            progression_rule(matrix, attribute, seed_list)
            
            seed_list = update_seedlist(seed_list)  # Update each time
            
        elif rule == Ruletype.DISTRIBUTE_THREE:
            distribute_three(matrix, attribute, binding_list, seed_list)
            seed_list = update_seedlist(seed_list)  # Update each time
        
    dis3_binding = check_binding(binding_list)
    print (dis3_binding)
    return matrix


def full_constant_rule(matrix, attribute, value):
    if value is not None:
        enum_class = ATTRIBUTE_TO_ENUM.get(attribute)#use the mapping dict to get the match the attribute to the class
        
        try:
            # Convert the string to uppercase and look up the corresponding enum value in the class
            constant_value = enum_class[value.upper()]
            
        except KeyError:
            raise ValueError(f"Invalid value '{value}' for {attribute.name}.")
    else:
        # If no value provided, use the existing attribute from the first matrix entity
        constant_value = getattr(matrix[0][0], attribute.name.lower()) 

    # Apply the constant value to all entities in the matrix
    for row in matrix:
        for entity in row:
            setattr(entity, attribute.name.lower(), constant_value)
            
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


       
def distribute_three(matrix, attribute, binding_list, seed_list):
    # Get the total number of unique attribute values
    max_value = len(globals()[attribute.name.capitalize() + "s"])
    potential_values = list(range(1, max_value + 1))

    # Get three unique values
    distribute_three_values, seed_list = get_random_attribute(seed_list, potential_values, number=3)
    
    # copy the values in a list and shuffle
    rows = [distribute_three_values[:]]  # Slice the entire, distribute_three_values list hereby essentialy copying it

    
    for _ in range(1, len(matrix)):  # Create the remaining rows with a cyclic shift
        new_row = rows[-1][1:] + rows[-1][:1]
        rows.append(new_row)
   
    rows, seed_list = random_shuffle(seed_list, rows)  # Shuffle row order for randomness
    

# Get the diagonal, then save the direction in binding list. 
    np_matrix = np.array(rows)
    diagonal = np.diagonal(np_matrix)
    if len(np.unique(diagonal)) > 1:
        binding_list.append ('lower')
    elif len(np.unique(diagonal)) <= 1:
        binding_list.append ('upper')
    
    
    # Assign values to entities
    for row, row_values in zip(matrix, rows):
        
        for i, entity in enumerate(row):
            value_to_assign = row_values[i]

            # Find the corresponding enum member and set the attribute
            for enum_member in globals()[attribute.name.capitalize() + "s"]:
                if enum_member.value == value_to_assign:
                    setattr(entity, attribute.name.lower(), enum_member)
                    break
            else:
                raise ValueError(f"No matching enum value found for {value_to_assign}.")

    return binding_list  

def check_binding(binding_list):
    """
    Checks the binding list. If at least two elements are the same ('upper' or 'lower'),
    it indicates binding.

    Parameters:
    binding_list (list of str): A list containing 'upper' or 'lower' strings.

    Returns:
    bool: True if binding is occurring (at least two values are the same), False otherwise.
    """
    unique_elements, counts = np.unique(binding_list, return_counts=True)
    return any(count >= 2 for count in counts)  # True if any element appears at least twice
  