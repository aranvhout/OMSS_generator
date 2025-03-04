from enum import Enum, auto
from typing import Optional
from entity import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linelengths, Linewidths,  Linenumbers
from seed import random_choice, update_seedlist, random_shuffle
import numpy as np


class AttributeType(Enum):
    SHAPE = auto()        
    SIZE = auto()
    COLOR = auto()
    ANGLE = auto()
    POSITION = auto ()
    LINETYPE = auto ()
    LINEWIDTH = auto ()
    LINELENGTH = auto ()
    LINENUMBER = auto ()
        
class Ruletype(Enum):
    CONSTANT = auto()
    FULL_CONSTANT = auto ()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()
    
#dict matching attributetypes (the stuff the user specifies) to classes (which contain the values etc)   
ATTRIBUTETYPE_TO_ENUM = {
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

class Rule:
    def __init__(self, rule_type: Ruletype, attribute_type: AttributeType, value: Optional[str] = None): #value is only relevant for the full_constant rule
        self.rule_type = rule_type
        self.attribute_type = attribute_type
        self.value = value  # Optional additional value    
  
def apply_rules(matrix, rules, seed_list):
    binding_list = [] #for now this is only relevant for dist3, basically it checks whether is binding going on
    
    for rule_obj in rules:
        rule = rule_obj.rule_type  # Accessing rule_type from Rule object
        attribute_type = rule_obj.attribute_type
        value = rule_obj.value  # Optional additional value
                
        if rule == Ruletype.CONSTANT:
            constant_rule(matrix, attribute_type, seed_list)
            
        elif rule == Ruletype.FULL_CONSTANT:
            full_constant_rule(matrix, attribute_type, value)
              
        elif rule == Ruletype.PROGRESSION:
            progression_rule(matrix, attribute_type, seed_list)
            
            seed_list = update_seedlist(seed_list)  # Update each time
            
        elif rule == Ruletype.DISTRIBUTE_THREE:
            distribute_three(matrix, attribute_type, binding_list, seed_list)
            seed_list = update_seedlist(seed_list)  # Update each time
        
    dis3_binding = check_binding(binding_list)
    
    return matrix

def full_constant_rule(matrix, attribute_type, value):
    if value is not None:
        enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)#use the mapping dict to get the match the attribute to the class
        
        try:
            # Convert the string to uppercase and look up the corresponding enum value in the class
            constant_value = enum_class[value.upper()]
            
        except KeyError:
            raise ValueError(f"Invalid value '{value}' for {attribute_type.name}.")
    else:
        # If no value provided, use the existing attribute from the first matrix entity
        constant_value = getattr(matrix[0][0], attribute_type.name.lower()) 

    # Apply the constant value to all entities in the matrix
    for row in matrix:
        for entity in row:
            setattr(entity, attribute_type.name.lower(), constant_value)
            
#CONSTANT            
def constant_rule(matrix, attribute_type, seed_list):   
    # Get the Enum class based on the attribute
   enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type, None)
   
   if enum_class is None:
       raise ValueError(f"Unknown attribute: {attribute_type.name}")

   # List all values of the specified attribute class
   values = list(enum_class)
   n_values = len(values)
   
   for row in matrix:
       constant_value, seed_value = random_choice(seed_list, values)
       if n_values >=3: 
           values.remove (constant_value)# remove it so we get unique values for each row, only remove it when we the attribute does have 3 instances at least
        
        # Set this constant value for the specified attribute across all entities in the row
       for entity in row:
            setattr(entity, attribute_type.name.lower(), constant_value)
        
            
#PROGRESSION        
def progression_rule(matrix, attribute_type, seed_list):
    """Applies a progression rule across each row for a given attribute."""
    
    # Get the maximum value, step size, and direction for the progression
    max_value, step_size, direction, seed_list = determine_progression_params(attribute_type, seed_list)
    start_values = determine_starting_values(attribute_type, max_value, step_size, direction)  
                   
        
    for row in matrix:            
            
        start_values, seed_list = adjust_starting_entity(row[0], attribute_type, start_values, seed_list)#adjusts the entity and updates the start values
        
        
        # Get the starting value and apply progression across the row
        current_value = getattr(row[0], attribute_type.name.lower()).value
       
        for i, entity in enumerate(row):
            # Calculate the new value using the progression formula
            new_value = (current_value + i * step_size * direction) 
            
            #the next part ensures that we can cycle in case of position or angle
            if new_value > max_value and attribute_type in (AttributeType.POSITION, AttributeType.ANGLE): #in case of upward progression
                new_value = new_value - max_value
            
            if new_value <1 and max_value and attribute_type in (AttributeType.POSITION, AttributeType.ANGLE): #in case of downward progression
                new_value = new_value + max_value
           
            
            # Get the corresponding Enum class from the dictionary using the attribute_type
            enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
           
            # If the attribute_type is not in the dictionary, raise an error
            if enum_class is None:
                raise ValueError(f"Unknown attribute type: {attribute_type.name}")

            # Now, iterate through the Enum members of the enum_class to find the matching value
            for enum_member in enum_class:           
                if enum_member.value == new_value:
                    setattr(entity, attribute_type.name.lower(), enum_member)
                    break
            else:
                    # If no matching value is found, raise an error
                raise ValueError(f"No matching enum value found for {new_value} in {attribute_type.name}.", attribute_type)
                   
                       
            
                
def determine_progression_params(attribute_type, seed_list):
    """Determines the max steps, step size, and direction for a given attribute type to make the progression rule work."""
    enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
    max_value = len(enum_class) 
        
    if max_value <7:
        possible_step_sizes = [1] #if we want each row to start with a different attribute, we need atleast 7 options for a 2-size progression
  
    if max_value >7:
        possible_step_sizes = [1,1,2]#in cases of 7 options can progress with 2, however I increased the numbers of 1, making a smaller progression more likely
         
          
    
    # based on seed chose step_size and direction        
    step_size, seed_list = random_choice(seed_list, possible_step_sizes)
    direction, seed_list = random_choice(seed_list, [-1,1])
    
    return max_value, step_size, direction, seed_list

def determine_starting_values ( attribute_type, max_value, step_size, direction):
    'creates a list of potential starting values'
    enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
    
    if attribute_type in (AttributeType.POSITION, AttributeType.ANGLE): #these attributes can progress indefinitely so we need a slighlty different logic, firstly each starting value should be possible  
        start_value_list = []        
        for value in enum_class:
            start_value_list.append(value.value)       
          
    else:
        start_value_list = []
        if direction == 1: #upward progression
            for value in enum_class:
                if value.value + (step_size * 2) <= max_value:
                    start_value_list.append(value.value)
                
        elif direction == -1: #downward progression
            for value in enum_class:
                if value.value + (step_size * - 2) >=1:  # If it stays larger than 1, enum starts at 1
                    start_value_list.append(value.value)
   
    
        #safety to make sure there will always be enough values 
        i = 0
        while len(start_value_list) < 3:
            start_value_list.append(start_value_list[i]) #no need for randomness since we randomly sample later
            i += 1
            print('increase by', i, 'values')
              
    return start_value_list
    
def adjust_starting_entity(entity, attribute_type, start_value_list, seed_list):
    "select value from the start value_list and set it as starting value"   
    
    start_value, seed_list  = random_choice(seed_list, start_value_list)
    start_value_list.remove(start_value)
    enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
    # Set the adjusted current value back to the entity
    for enum_member in enum_class:
     if enum_member.value == start_value:
         #print(enum_member, current_value, step_size, potential_value)
         setattr(entity, attribute_type.name.lower(), enum_member)     
         break
        
    
    else:
        raise ValueError(f"No matching enum value found for {start_value}.")
       
    return start_value_list, seed_list


#distribute three       
def distribute_three(matrix, attribute_type, binding_list, seed_list):
    # Get the total number of unique attribute values
    enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
    max_value = len(enum_class)
    potential_values = list(range(1, max_value + 1))

    # Get three unique values
    distribute_three_values, seed_list = random_choice(seed_list, potential_values, number=3)
    
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
            for enum_member in enum_class:
                if enum_member.value == value_to_assign:
                    setattr(entity, attribute_type.name.lower(), enum_member)
                    break
            else:
                raise ValueError(f"No matching enum value found for {value_to_assign}.")

    return binding_list  

def check_binding(binding_list):
    """
    Checks the binding list for dist3. If at least two elements are the same ('upper' or 'lower'),
    it indicates binding.

   
    """
    unique_elements, counts = np.unique(binding_list, return_counts=True)
    return any(count >= 2 for count in counts)  # True if any element appears at least twice
  