from rules import Ruletype, AttributeType, apply_rules
from seed import seed_generator
from entity import create_random_entity
import sys, cv2
from render import render_matrix


n_iteration=0 #create global iteration variable

# Function to create a matrix of entities (BigShape or Line)
def create_matrix(num_rows, num_columns, rules, seed=None, entity_type="big-shape"): 
    global n_iteration
    seed_list = seed_generator(seed)
    
    # Initialize a random starting matrix
    starting_matrix = create_starting_matrix(num_rows, num_columns, seed_list, entity_type)   
    matrix = apply_rules (starting_matrix, rules, seed_list)   
                   
        
    # check whether the random aspects in the matrix follow any accidental patterns
    if validate_matrix(matrix, rules, seed): #if there a no non-intended patterns occuring return true
        print('matrix created') 
        row_lengths = [(0, 3), (0, 3), (0, 3)] 
        rendered_solution_matrix = render_matrix (matrix, row_lengths)
        output_path_with_lines = "solution_matrix.png"
        cv2.imwrite(output_path_with_lines, rendered_solution_matrix)
        
        row_lengths = [(0, 3), (0, 3), (0, 2)] 
        rendered_solution_matrix = render_matrix (matrix, row_lengths)
        output_path_with_lines = "problem_matrix.png"
        cv2.imwrite(output_path_with_lines, rendered_solution_matrix)
                     
        
        n_iteration=0
        return matrix
        
    
    # If there a non-intended paterns, try again (and if seed is not None, adjust the seed)
    n_iteration += 117 # weird value, I want to avoid for example seed 3 and 4 being the same on the user end
    if n_iteration < 117 * 11:
        # Pass modified seed if initial seed is not None
        new_seed = seed + n_iteration if seed is not None else None
        return create_matrix(num_rows, rules, new_seed)
    
    # If max retries reached, fail gracefully
    print('Matrix could not be created after multiple attempts.')
    sys.exit()

   
def validate_matrix(matrix, rules, seed): #wrapper function to check whether the random-rule attribute combination yields accidental patterns
    for rule, attribute in rules:
        if rule is Ruletype.RANDOM and attribute is AttributeType.SHAPE: 
            if not check_rules(matrix, attribute):
                print('shape check_rules failed, retrying...')
                return False  # Exit if check_rules fails
            print('shape checked')

        if rule is Ruletype.RANDOM and attribute is AttributeType.SIZE:
            if not check_rules(matrix, attribute):
                print('size check_rules failed, retrying...')
                return False  # Exit if check_rules fails
            print('size checked')

        if rule is Ruletype.RANDOM and attribute is AttributeType.COLOR:
            if not check_rules(matrix, attribute):
                print('color check_rules failed, retrying...')
                return False  # Exit if check_rules fails
            print('color checked')

        if rule is Ruletype.RANDOM and attribute is AttributeType.ANGLE:
            if not check_rules(matrix, attribute):
                print('angle check_rules failed, retrying...')
                return False  # Exit if check_rules fails
            print('angle checked')
    
  
    return True  # All check_ruless passed
            
def check_rules(matrix, attribute): 
       
    # 1 Create matrix with numbers associated with each attribute that is being checked
    numerical_matrix=[]  
    for row in matrix:
        numerical_row=[]
        for entity in row:
            attribute_name = attribute.name.lower()  # Convert enum name to lowercase to match attribute name in Entity
            attribute_value = getattr(entity, attribute_name)  # Access the attribute dynamically           
            numerical_row.append(attribute_value.value)
            
        numerical_matrix.append(numerical_row)    
    numerical_matrix[2].pop()#remove the answer entity (this should not be included in the checks)
   
        
    #check constant rule  
    constant = True   
    for row in numerical_matrix:
        if len(set(row)) > 1: 
            constant = False        
            break     
               
     # Check upward progression
    upward_progression = True
    for row in numerical_matrix:
        for i in range(len(row) - 1): 
            if row[i] >= row[i + 1]: #any upward progression, I'm for now ignoring stepsize 
                upward_progression = False
                break  # Exit the inner loop if not progressing
        if not upward_progression:
            break  # Exit the outer loop if a non-progressing row is found
            
     # Check downward progression       
    downward_progression = True
    for row in numerical_matrix:
        for i in range(len(row) - 1): 
            if row[i] <= row[i + 1]:  
                downward_progression = False
                break  # Exit the inner loop if not progressing
        if not downward_progression:
            break  # Exit the outer loop if a non-progressing row is found 
      
    #check distribute three
    distribute_three = True
    reference_row = numerical_matrix[0]

    for row in numerical_matrix[1:]:
        # Check if all values in row exist in reference_row and are unique in the row
        if not all(value in reference_row for value in row) or len(row) != len(set(row)):
            distribute_three = False
            break
  
    
    #check distribute two (not sure whether to include this yet) also i think this does need to check the whole matrix instead of the popped matrix
    distribute_two = True   
    common_elements = set(numerical_matrix[0])  # Initialize with the first row
    for row in numerical_matrix[1:]:
        common_elements.intersection_update(row)  # neved heard of this method but it is exactly what we need
    if len(common_elements) <2:
        distribute_two = False
    
    #check whether all checks are negative
    if constant or upward_progression or downward_progression or distribute_three or distribute_two:
        print(attribute, constant , upward_progression , downward_progression , distribute_three , distribute_two)
        print(numerical_matrix)
        for row_index, row in enumerate(matrix):
            print(f"\nRow {row_index + 1}:")
            for i, entity in enumerate(row):
                print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")    
        return False
        
    return True
    
        
def create_starting_matrix(n_rows=3, n_columns=3, seed_list=None, entity_type="big-shape"):
    matrix = []
    for i in range(n_rows):
        row = []
        for j in range(n_columns):
            entity, seed_list = create_random_entity(seed_list, entity_type)  # Specify entity_type (BigShape or Line)
            row.append(entity)
        matrix.append(row)
    return matrix


    
    
    
  
    