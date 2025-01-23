from rules import Ruletype, AttributeType, apply_rules, Rule
from seed import seed_generator
from entity import create_random_entity
import sys, cv2
from render import render_matrix


n_iteration=0 #create global iteration variable

# Function to create a matrix of entities (BigShape or Line)
def create_matrix(num_rows, num_columns, rules, seed=None, entity_types=["big-shape"]): 
    
    matrices = {}  # To store valid matrices
    
    for entity_type in entity_types:
        if entity_type not in rules:
            raise ValueError(f"No rules defined for entity type: {entity_type}")
        entity_rules = rules[entity_type]
        n_iteration = 0  # Track adjustments for seed
        attempt = 0  # Track retries for each entity type
        
        while entity_type not in matrices and attempt < 11:
            # Generate seed list
            seed_list = seed_generator(seed + n_iteration if seed is not None else seed)
            # Create a starting matrix for the current entity type
            starting_matrix = create_starting_matrix(entity_rules, num_rows, num_columns, seed_list, entity_type)#note to self. entity type defined in the for-loop 
            # Apply rules to the starting matrix
            matrix = apply_rules(starting_matrix, entity_rules, seed_list)
            
            # Validate the matrix
            if validate_matrix(matrix, entity_rules, seed):
                matrices[entity_type] = matrix  # Save the valid matrix
                
                
       
            else:
                # Adjust seed if necessary and retry
                n_iteration += 117
                attempt += 1
        
    # Check if any entity types failed to generate a valid matrix
    if len(matrices) != len(entity_types):
        raise ValueError("Unable to generate valid matrices for all specified entity types after multiple attempts")
    else:
        row_lengths = [(0, 3), (0, 3), (0,3)] 
        rendered_solution_matrix = render_matrix (matrices,)
        output_path_with_lines = "solution_matrix.png"
        cv2.imwrite(output_path_with_lines, rendered_solution_matrix)

        
    print(matrices)  
    return matrices

   
def validate_matrix(matrix, rules, seed): #wrapper function to check whether the random-rule attribute combination yields accidental patterns
    for rule_obj in rules:
        rule = rule_obj.rule_type  # Accessing the rule type from the Rule object
        attribute = rule_obj.attribute  # Accessing the attribute from the Rule object
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
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.LINETYPE:
            if not check_rules(matrix, attribute):
                print('linetype check_rules failed, retrying...')
                return False  # Exit if check_rules fails
            print('linetype checked')
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.LINEWIDTH:
            if not check_rules(matrix, attribute):
                print('linewidth check_rules failed, retrying...')
                return False  # Exit if check_rules fails
            print('linewidth checked')
            
            
    
  
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
        
        for row_index, row in enumerate(matrix):
            print(f"\nRow {row_index + 1}:")
            for i, entity in enumerate(row):
                print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")   
                #print(f"  Entity {i + 1}: Color={entity.color}, Linewidth={entity.linewidth}, Linetype={entity.linetype}")   
        return False
        
    return True
    
        
def create_starting_matrix(rules, n_rows=3, n_columns=3, seed_list=None, entity_type=["big-shape"]):
    matrix = []
    for i in range(n_rows):
        row = []
        for j in range(n_columns):
            if not any(rule.attribute == AttributeType.POSITION for rule in rules):
                entity, seed_list = create_random_entity(seed_list, entity_type)#  Default position
                
            else:                
                entity, seed_list = create_random_entity(seed_list, entity_type, position = "random" ) # Random position
                
            row.append(entity)
        matrix.append(row)
    return matrix 


    
    
    
  
    