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
            constant_rule(matrix, attribute, seed_list)
            
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
def constant_rule(matrix, attribute, seed_list):   
    #1 list all values of class
    values=[]
    
    for enum_member in globals()[attribute.name.capitalize() + "s"]:
        values.append(enum_member)
   
    n_values =len(values)
   
    for row in matrix:
        constant_value, seed_value = get_random_attribute(seed_list, values)
        if n_values >=3: 
            values.remove (constant_value)# remove it so we get unique values for each row, only remove it when we the attribute does have 3 instances at least
        
        # Set this constant value for the specified attribute across all entities in the row
        for entity in row:
            setattr(entity, attribute.name.lower(), constant_value)
            
#PROGRESSION    
    
def progression_rule(matrix, attribute, seed_list):
    """Applies a progression rule across each row for a given attribute."""
    
    # Get the maximum value, step size, and direction for the progression
    max_value, step_size, direction, seed_list = determine_progression_params(attribute, seed_list)
    start_values = determine_starting_values( attribute, max_value, step_size, direction)  
    
        
        
        
    for row in matrix:    
        
            
        start_values, seed_list = adjust_starting_entity(row[0], attribute, start_values, seed_list)#adjusts the entity and updates the start values
        
        
        # Get the starting value and apply progression across the row
        current_value = getattr(row[0], attribute.name.lower()).value
       
        for i, entity in enumerate(row):
            # Calculate the new value using the progression formula
            new_value = (current_value + i * step_size * direction) 
            
            #the next part ensures that we can cycle in case of position or angle
            if new_value > max_value and attribute in (AttributeType.POSITION, AttributeType.ANGLE): #in case of upward progression
                new_value = new_value - max_value
            
            if new_value <1 and max_value and attribute in (AttributeType.POSITION, AttributeType.ANGLE): #in case of downward progression
                new_value = new_value + max_value
           
            # Set the new value to the entity, using the corresponding enum
            for enum_member in globals()[attribute.name.capitalize() + "s"]:
                if enum_member.value == new_value:
                    setattr(entity, attribute.name.lower(), enum_member)
                    break
            else:                    
                raise ValueError(f"No matching enum value found for {new_value}.", attribute) 
                
def determine_progression_params(attribute, seed_list):
    """Determines the max steps, step size, and direction for a given attribute type to make the progression rule work."""
    max_value = len(globals()[attribute.name.capitalize() + "s"])#this line works, chatgpt came up with it, i dont fully understand the globals part
    
    if max_value <7:
        possible_step_sizes = [1] #if we want each row to start with a different attribute, we need atleast 7 options for a 2-size progression
  
    if max_value >7:
        possible_step_sizes = [1,1,2]#in cases of 7 options can progress with 2, however I increased the numbers of 1, making a smaller progression more likely
   
       
          
    
    # based on seed chose step_size and direction        
    step_size, seed_list = get_random_attribute(seed_list, possible_step_sizes)
    direction, seed_list = get_random_attribute(seed_list, [-1,1])
    
    return max_value, step_size, direction, seed_list

def determine_starting_values ( attribute, max_value, step_size, direction):
    'creates a list of potential starting values'
    if attribute in (AttributeType.POSITION, AttributeType.ANGLE): #these attributes can progress indefinitely so we need a slighlty different logic, firstly each starting value should be possible  
        start_value_list = []
        for value in (globals()[attribute.name.capitalize() + "s"]):
            start_value_list.append(value.value)       
    
       
    else:
        start_value_list = []
        if direction == 1: #upward progression
            for value in (globals()[attribute.name.capitalize() + "s"]):
                if value.value + (step_size * 2) <= max_value:
                    start_value_list.append(value.value)
                
        elif direction == -1: #downward progression
            for value in (globals()[attribute.name.capitalize() + "s"]):
                if value.value + (step_size * - 2) >=1:  # If it stays larger than 1, enum starts at 1
                    start_value_list.append(value.value)
   
    
        #safety to make sure there will always be enough values 
        i = 0
        while len(start_value_list) < 3:
            start_value_list.append(start_value_list[i]) #no need for randomness since we randomly sample later
            i += 1
            print('increase by', i, 'values')
              
    return start_value_list
    
def adjust_starting_entity(entity, attribute, start_value_list, seed_list):
    "select value from the start value_list and set it as starting value"   
    
    start_value, seed_list  = get_random_attribute(seed_list, start_value_list)
    start_value_list.remove(start_value)
       
    # Set the adjusted current value back to the entity
    for enum_member in globals()[attribute.name.capitalize() + "s"]:
     if enum_member.value == start_value:
         #print(enum_member, current_value, step_size, potential_value)
         setattr(entity, attribute.name.lower(), enum_member)     
         break
        
    
    else:
        print(enum_member)
        raise ValueError(f"No matching enum value found for {start_value}.")
       
    return start_value_list, seed_list


       
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
  