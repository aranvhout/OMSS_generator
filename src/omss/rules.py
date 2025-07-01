#OMSS imports
from .element import Shapes, Sizes, Colors, Angles, Positions, Linetypes,  Linenumbers, Bigshapenumbers, Littleshapenumbers, LittleShape
from .seed import random_choice, update_seedlist, random_shuffle

#general imports
from enum import Enum, auto
from typing import Optional

from copy import deepcopy
import numpy as np
from itertools import product
import sys

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
    NUMBER = auto ()
    LITTLESHAPENUMBER = auto ()
        
class Ruletype(Enum):
    CONSTANT = auto()
    FULL_CONSTANT = auto ()
    PROGRESSION = auto()
    DISTRIBUTE_THREE = auto()
    ARITHMETIC = auto ()
    
#dict matching attributetypes (the stuff the user specifies) to classes (which contain the values etc)   
ATTRIBUTETYPE_TO_ENUM = {
    AttributeType.COLOR: Colors,
    AttributeType.SHAPE: Shapes,
    AttributeType.SIZE: Sizes,
    AttributeType.ANGLE: Angles,
    AttributeType.POSITION: Positions,
    AttributeType.LINETYPE: Linetypes,
    AttributeType.LINENUMBER: Linenumbers,
    AttributeType.NUMBER: Bigshapenumbers,
    AttributeType.LITTLESHAPENUMBER: Littleshapenumbers,
}

class Rule:
    def __init__(self, rule_type: Ruletype, attribute_type: Optional[AttributeType] = None, value: Optional[str] = None, direction: Optional[str] = None, arithmetic_layout: Optional = None,  excluded: Optional = None): #value is only relevant for the full_constant rule
        self.rule_type = rule_type
        self.attribute_type = attribute_type
        self.value = value  
        self.direction = direction #maybe relevant for progression as well
        self.arithmetic_layout = arithmetic_layout
        self.excluded = excluded #excluded instances (eg could be certain colours that can't used whatever)
     
    def __repr__(self):
        return (f"Rule(rule_type={self.rule_type}, attribute_type={self.attribute_type}, value={self.value}, "
                f"direction={self.direction}, arithmetic_layout={self.arithmetic_layout}, excluded={self.excluded})") 
class Configuration:
    def __init__(self, alternative_indices):
        self.alternative_indices = alternative_indices

    def __repr__(self):
        return f"Configuration(alternative_indices={self.alternative_indices})"
       
     

        
def apply_rules(matrix, element_rules, seed_list):
    
    binding_list =[]
    
    for rule_obj in element_rules:
        if isinstance(rule_obj, Rule):
            rule = rule_obj.rule_type  # Accessing rule_type from Rule object        
            attribute_type = rule_obj.attribute_type
            value = rule_obj.value  # Optional additional value
            direction = rule_obj.direction
            arithmetic_layout = rule_obj.arithmetic_layout
            excluded = rule_obj.excluded
            
       
            if rule == Ruletype.ARITHMETIC:                      
                seed_list = arithmetic_rule (matrix, attribute_type, arithmetic_layout, direction, seed_list)
                seed_list = update_seedlist(seed_list)        
                
            elif rule == Ruletype.CONSTANT:
                matrix, seed_list = constant_rule(matrix, attribute_type, seed_list)
                seed_list = update_seedlist(seed_list)
                
            elif rule == Ruletype.FULL_CONSTANT:
                full_constant_rule(matrix, attribute_type, value)
              
            elif rule == Ruletype.PROGRESSION:
                progression_rule(matrix, attribute_type, seed_list)            
                seed_list = update_seedlist(seed_list)  # Update each time
            
            elif rule == Ruletype.DISTRIBUTE_THREE:
                distribute_three(matrix, attribute_type, binding_list, seed_list)
                seed_list = update_seedlist(seed_list)  # Update each time
            
        
        dis3_binding = check_binding(binding_list)#might be relecant for a later stage
        # Only apply if matrix contains LittleShape objects
    if isinstance(matrix[0][0], LittleShape):
       seed_list = number2position(element_rules, matrix, seed_list)
  
    return matrix, seed_list


def number2position(element_rules, matrix, seed_list):
    'this function matches number elements (eg line and littleshape) to positions within the grid'

    # Decide direction once: randomly pick clockwise or counterclockwise
    direction, seed_list = random_choice(seed_list, ['clockwise', 'counterclockwise'])

    for row in matrix:
        numbered_elements = [
            element for element in row
            if element.littleshapenumber is not None
        ]

        numbers = [element.littleshapenumber.value for element in numbered_elements]

        rule = next(
            (rule.rule_type for rule in element_rules if rule.attribute_type == AttributeType.LITTLESHAPENUMBER),
            None
        )

        positions, seed_list = coupling(rule, numbers, direction, seed_list)

        # Only assign positions to numbered elements
        for element, pos in zip(numbered_elements, positions):
            setattr(element, 'position', pos)

    return seed_list


        

    return seed_list


def coupling(rule, numbers, direction, seed_list):
    'matches the numbers to a specific position'

    max_number = max(numbers)
    max_indices = [i for i, n in enumerate(numbers) if n == max_number]

    position_values = list(Positions)  # enum members

    cycle_positions = [
        Positions.TOP_LEFT,
        Positions.TOP_RIGHT,
        Positions.BOTTOM_RIGHT,
        Positions.BOTTOM_LEFT,
    ]

    # Reverse cycle if direction is counterclockwise
    if direction == 'counterclockwise':
        cycle_positions = list(reversed(cycle_positions))

    def get_contiguous_positions(cycle, start_pos, length, seed_list):
        start_idx = cycle.index(start_pos)
        return [cycle[(start_idx + i) % len(cycle)] for i in range(length)], seed_list

    if rule == Ruletype.CONSTANT:
        if len(set(numbers)) != 1:
            raise ValueError("All numbers must be the same for CONSTANT rule.")
        shared, seed_list = random_choice(seed_list, position_values, numbers[0])
        return [shared for _ in numbers], seed_list

    if rule == Ruletype.DISTRIBUTE_THREE:
        
        result = []
        for num in numbers:
            position, seed_list = random_choice(seed_list, position_values, num)
            result.append(position)
        return result, seed_list

    # Now handle ARITHMETIC with 2 or 3 numbers

    max_idx = max_indices[0]
    result = [None] * len(numbers)

    start_pos, seed_list = random_choice(seed_list, cycle_positions)
    max_pos, seed_list = get_contiguous_positions(cycle_positions, start_pos, max_number, seed_list)
    result[max_idx] = max_pos

    rest = [i for i in range(len(numbers)) if i != max_idx]

    if rule == Ruletype.ARITHMETIC:
        if len(numbers) == 2:
            result[0] = max_pos
            result[1] = result[0] 
            

        elif len(numbers) == 3:
            n1, n2 = numbers[rest[0]], numbers[rest[1]]
            sorted_pos = sorted(max_pos, key=lambda p: p.value)
            result[rest[0]] = sorted_pos[:n1]
            result[rest[1]] = sorted_pos[-n2:]

    elif rule == Ruletype.PROGRESSION:
        # Your original progression logic remains untouched here
        result[rest[0]], seed_list = get_contiguous_positions(cycle_positions, start_pos, numbers[rest[0]], seed_list)
        result[rest[1]], seed_list = get_contiguous_positions(cycle_positions, start_pos, numbers[rest[1]], seed_list)

    return result, seed_list






    
    
#FULL_CONSTANT
def full_constant_rule(matrix, attribute_type, value):
    if value is not None:
        enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)#use the mapping dict to get the match the attribute to the class
        
        try:
            # Convert the string to uppercase and look up the corresponding enum value in the class
            constant_value = enum_class[value.upper()]
            
        except KeyError:
            raise ValueError(f"Invalid value '{value}' for {attribute_type.name}.")
    else:
        # If no value provided, use the existing attribute from the first matrix element
        constant_value = getattr(matrix[0][0], attribute_type.name.lower()) 

    # Apply the constant value to all elements in the matrix
    for row in matrix:
        for element in row:
            setattr(element, attribute_type.name.lower(), constant_value)
            
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
        
        # Set this constant value for the specified attribute across all elements in the row
       for element in row:
            setattr(element, attribute_type.name.lower(), constant_value)
   return matrix, seed_list
            
#PROGRESSION        
def progression_rule(matrix, attribute_type, seed_list):
    """Applies a progression rule across each row for a given attribute."""
    
    # Get the maximum value, step size, and direction for the progression
    max_value, step_size, direction, seed_list = determine_progression_params(attribute_type, seed_list)
    start_values = determine_starting_values(attribute_type, max_value, step_size, direction)  
                   
        
    for row in matrix:            
        start_values, seed_list = adjust_starting_element(row[0], attribute_type, start_values, seed_list)#adjusts the element and updates the start values
                
        # Get the starting value and apply progression across the row
        current_value = getattr(row[0], attribute_type.name.lower()).value
       
        for i, element in enumerate(row):
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
                    setattr(element, attribute_type.name.lower(), enum_member)
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
            
              
    return start_value_list
    
def adjust_starting_element(element, attribute_type, start_value_list, seed_list):
    "select value from the start value_list and set it as starting value"   
    
    start_value, seed_list  = random_choice(seed_list, start_value_list)
    start_value_list.remove(start_value)
    enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
    # Set the adjusted current value back to the element
    for enum_member in enum_class:
     if enum_member.value == start_value:
         #print(enum_member, current_value, step_size, potential_value)
         setattr(element, attribute_type.name.lower(), enum_member)     
         break
        
    
    else:
        raise ValueError(f"No matching enum value found for {start_value}.")
       
    return start_value_list, seed_list


#DISTRIBUTE_THREE     
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
    
    
    # Assign values to elements
    for row, row_values in zip(matrix, rows):
        
        for i, element in enumerate(row):
            value_to_assign = row_values[i]

            # Find the corresponding enum member and set the attribute
            for enum_member in enum_class:
                if enum_member.value == value_to_assign:
                    setattr(element, attribute_type.name.lower(), enum_member)
                    break
            else:
                raise ValueError(f"No matching enum value found for {value_to_assign}.")

    return binding_list  




#ARITHMETIC

def arithmetic_rule(matrix, attribute_type, layout, direction, seed_list):
    
    if layout is None: #layout is goverend by the configuration module      
           
        enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
        max_value = len(enum_class)
        potential_values = list(range(1, max_value + 1))        
        arithmetic_matrix, seed_list = arithmetic_operation(potential_values, direction, layout, seed_list)
        
        
        i = 0
        while arithmetic_matrix == False and i <10:
            seed_list = update_seedlist(seed_list)
            arithmetic_matrix, seed_list = arithmetic_operation(potential_values, direction, layout, seed_list)
            i+=1
        if not arithmetic_matrix:
            print("Failed to generate a arithmetic matrix without unintended rules after 10 attempts.")
            sys.exit(1)
            
    
        for row in matrix:
            for element in row:                
                r,c = element.element_index
                
                value_to_assign=arithmetic_matrix[r][c] 
                
                if value_to_assign == 0:
                    setattr(element, attribute_type.name.lower(), None)
                
                for enum_member in enum_class:                   
                    if enum_member.value == value_to_assign:
                        setattr(element, attribute_type.name.lower(), enum_member)
                  
        
    if layout is not None:   
        i=0
        enum_class = ATTRIBUTETYPE_TO_ENUM.get(attribute_type)
        max_value = len(enum_class)
        potential_values = list(range(1, max_value + 1))        
        arithmetic_matrix, seed_list = arithmetic_operation(potential_values, direction, layout, seed_list)
        while arithmetic_matrix == False and i <10:
            seed_list = update_seedlist(seed_list)
            arithmetic_matrix, seed_list = arithmetic_operation(potential_values, direction, layout, seed_list)
            i+=1
        if not arithmetic_matrix:
           print("Failed to generate a arithmetic matrix without unintended rules after 10 attempts.")
           sys.exit(1)
           
   
        for row in matrix:
            for element in row:                
                r,c = element.element_index
                value_to_assign=arithmetic_matrix[r][c] 
                if value_to_assign == 0:
                    setattr(element, attribute_type.name.lower(), None)
                
                for enum_member in enum_class:                   
                    if enum_member.value == value_to_assign:
                        setattr(element, attribute_type.name.lower(), enum_member)      
        
        
      
        
        
        
        pass
    
    return seed_list
        
def arithmetic_operation(potential_values, direction, layout,  seed_list):
    if layout is not None and len(potential_values) <=3:
        min_value = 0
        answer_excluded = 0 #aka no answer excluded
    
    elif layout is not None and len(potential_values)>3:#reduce the change of a '1' if there are other options since it results in forced zero values
        change_number_list = [0,0,0,1,1,1,1,1,1,1] #70percent change of selecting 1 
        answer_excluded, seed_list = random_choice(seed_list, change_number_list) #70 percent of the times 1 is excluded as an answer beforehand
        min_value = 0
        
    else:#in case of no layout, we we will never allow an answer of 1 (we cant have zero values)
        answer_excluded = 1
        min_value = 1      
                

    # Calculate potential endings, keep them as different as possible while allowing addition to be possible
   
    answers, seed_list = random_choice(seed_list, potential_values, number=3, exclude=[answer_excluded])
    
    potential_operands = []
           
        
   
    rows = [0, 1, 2]  
    
    # Generate potential operands
    potential_operands = []
    for answer_index, answer in enumerate(answers):  
        row = rows[answer_index]  # Assign the correct row for this answer

        for i in range(min_value, answer):
            j = answer - i
            if j >= i:  
                pair = [row, answer, i, j]  
                if pair not in potential_operands:
                    potential_operands.append(pair)

            if i != j:  
                reversed_pair = [row, answer, j, i]
                if reversed_pair not in potential_operands:
                    potential_operands.append(reversed_pair)

    
    # Filter out invalid operands based on layout
    filtered_operands = []
    for operand in potential_operands:
        row = operand[0]  # First value is the row index
        values = operand[1:]  # Remaining values are the numbers in that row

        valid = True
        # Loop through each value in the operand
        for col_index in range(len(values)):
            value = values[col_index]
           
            # Check if this value is zero and if its position (row, col_index+1) is in layout
            if value == 0 and (row, col_index) not in layout:
                valid = False
                
                break  # No need to check further if it's invalid

        if valid:
            filtered_operands.append(operand)
     
    #

        
   
    #add a shuffle here to get some randomness    
    filtered_operands, seed_list =random_shuffle (seed_list, filtered_operands)   
        
    answers, seed_list =random_shuffle (seed_list, answers)
    
    #get the most unique selection
    result= arithmetic_selection(filtered_operands, answers)
    
    if direction == 'addition':
        #try except sstructure, we can have an error in case we dotn create a valid matrix, however this is adressed later on
        try:
            # Reverse each sublist in result
            result = [sublist[::-1] for sublist in result]
        except TypeError:
            pass  # Ignore the error and continue

        
    return result, seed_list           
        


def arithmetic_selection(lst, answers):
   
    # step 1, reduce the number of the zero possibilities
    row_groups = {}
    for sublist in lst:
        row_groups.setdefault(sublist[0], []).append(sublist)  # Use 1nd number for grouping (aka the row number)           
      
    zero = True # we use this to allow one row to contain zero values as long as there are enough options
    for key in list(row_groups):  
        if len(row_groups[key]) > 1 and not zero:
            filtered = [operand for operand in row_groups[key] if 0 not in operand]
        
            # Ensure at least one value remains
            if filtered:
                row_groups[key] = filtered  
            else:
                row_groups[key] = [row_groups[key][0]]  # Keep one original value
        else:
            zero = False
    
    

     
    selected_values = [value for sublist in row_groups.values() for value in sublist]
   
    # Step 2: Group lists by first index
         
    first_index_groups = {}
    for sublist in selected_values:
        first_index_groups.setdefault(sublist[1], []).append(sublist)  # Use 2nd number for grouping (aka the answer number)
                             
            
       
    best_selection = None
    best_uniqueness_score = -1

    # Step 2: Get all possible selections based on provided first indices
    possible_selections = [first_index_groups[i] for i in answers if i in first_index_groups]
    
    if len(possible_selections) < 3:
        return None  # Not enough valid groups to pick from

    # Step 3: Try all combinations of picking one from each group
    for choice in product(*possible_selections):
        
        row_set = {x[0] for x in choice}  # Get the unique row indices
        
        if len(row_set) < len(choice):  
            
            continue  # Skip selections with duplicate rows
        
        # Measure uniqueness in second and third indices
        second_index_set = {x[2] for x in choice}
        third_index_set = {x[3] for x in choice}

        # Adjusted uniqueness scoring
        uniqueness_score = (len(second_index_set) if len(second_index_set) > 1 else 0) + \
                           (len(third_index_set) if len(third_index_set) > 1 else 0)
        
        # Keep the selection with the best uniqueness score
        if uniqueness_score > best_uniqueness_score:
            best_uniqueness_score = uniqueness_score
            best_selection = choice
            
     
    if best_selection:
        best_selection = sorted(best_selection, key=lambda x: x[0])
    
    # **Remove the first value (row index) only after sorting**
    best_selection_no_row_value = [selection[1:] for selection in best_selection] if best_selection else None
    
    #do some check to prevent accidental rules from happening
    valid_matrix = check_for_rules(best_selection_no_row_value)
    if valid_matrix is False: #some cool recursion
        
        return False
 
    
      
    
    
    
    
    
    
    
    
    return best_selection_no_row_value

#





def check_for_rules (rows):
    
    rows_cut = [row[:] for row in rows]  # Create a deep copy of the rows list
    
    rows_cut[-1].pop()
    
    valid_matrix = False
 # Check downward progression       
    downward_progression = True
    for row in rows_cut:
        
        for i in range(len(row) - 1): 
            if row[i] <= row[i + 1]:  
                downward_progression = False
                break  # Exit the inner loop if not progressing
        if not downward_progression:
            break  # Exit the outer loop if a non-progressing row is found 
      

# Check upward progression
    upward_progression = True
    for row in rows_cut:
        for i in range(len(row) - 1): 
            if row[i] >= row[i + 1]: #any upward progression, I'm for now ignoring stepsize 
                upward_progression = False
                break  # Exit the inner loop if not progressing
        if not upward_progression:
            break  # Exit the outer loop if a non-progressing row is found
            
            
 #check distribute three
    distribute_three = True
    reference_row = rows_cut[0]

    for row in rows_cut[1:]:
        # Check if all values in row exist in reference_row and are unique in the row
        if not all(value in reference_row for value in row) or len(row) != len(set(row)):
            distribute_three = False
            break
        
    if upward_progression or downward_progression or distribute_three:
        print('unintended rule found, recreating')
        valid_matrix= False
        
    else:
        valid_matrix = True
        
    return valid_matrix
        
        
        
        
        
def check_binding(binding_list):
    """
    Checks the binding list for dist3. If at least two elements are the same ('upper' or 'lower'),
    it indicates binding.

   
    """
    unique_elements, counts = np.unique(binding_list, return_counts=True)
    return any(count >= 2 for count in counts)  # True if any element appears at least twice        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        




  