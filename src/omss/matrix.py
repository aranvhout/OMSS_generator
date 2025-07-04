#OMSS imports
from .rules import  AttributeType, apply_rules
from .seed import seed_generator
from .element import create_random_element, LittleShape
from .alternatives import create_alternatives
from .render import render_matrix, render_element
from .configuration import configuration_settings
from .rules import Rule

#general imports
import os
import cv2
import random
from pathlib import Path
 
def create_matrix( rules,  alternatives = None, seed=None, alternative_seed = None, save = True, output_file = False, element_types=None, path =None): 
    """Wrapping function that creates the matrix and alternatives"""
   
    # Generate seeds
    if seed  == None:
        seed = random.randint(0, 999999)        
       
    if alternative_seed == None:
        alternative_seed = random.randint(0, 999999)
    
    seed_list = seed_generator(seed) #use the seed to generate a seed list 
    
    # If element_types is not provided, infer from rules
    if element_types is None:
        element_types = list(rules.keys())
        
        
     # Path
    if path is None:
         path = Path.home() / "Documents" / "OMSS_output"
    else:
         path = Path(path)
    
    
    #This reviews the rules/matrices at the group settings. Allowing constraints in for element-type based upon another. For now this is only used for arithmetic
    updated_rules, seed_list = configuration_settings (rules, element_types, seed_list)
    
    matrices = {}  # dict to store valid matrices to be created
    
    # Step 4: superugly but we need to assign a position seed in case littleshape has an aritmetic
    

    # Create the directory if it doesn't exist
    path.mkdir(parents=True, exist_ok=True)
    
    #for loop that creates the matrix
    for element_type in element_types:
        
        if element_type not in updated_rules:
            raise ValueError(f"No rules defined for element type: {element_type}")
       
        element_rules = updated_rules[element_type]
                
        while element_type not in matrices:            
           # Create a starting matrix for the current element type
            starting_matrix = initialise_matrix(element_rules, seed_list, element_type)#note to self. element type defined in the for-loop 
            # Apply rules to the starting matrix
            matrix, seed_list = apply_rules(starting_matrix, element_rules, seed_list)   
            
            matrices[element_type] = matrix  # Save the valid matrix
    
    #we distuingish between saving and not saving. Saving will output the matrices in a folder, whereas not saving output the matrices and alternatives as variables the user can catch
    
    if save == True :
        save_matrices(matrices, path)
        if alternatives and alternatives > 1:
            LittleShape.reset_seed()
            LittleShape.set_seed(alternative_seed)#this is very ugly, we need to set a separate global seed for the position of little shape

            #create the alternatives and save the dissimilarity scores of the alternatives in a list
            dis_scores = generate_and_save_alternatives(matrices, element_types, alternatives, alternative_seed, updated_rules, path, save =True)
            
            if output_file == True: #creates output file contain info about the matrices etc                
                create_output_file(updated_rules, dis_scores, seed, alternative_seed, save, path)
        print('matrix created')
        
    if save == False:
        # Convert BGR to RGB
        solution_matrix_bgr = render_matrix(matrices)
        solution_matrix = cv2.cvtColor(solution_matrix_bgr, cv2.COLOR_BGR2RGB)
        problem_matrix_bgr = render_matrix(matrices, problem_matrix=True)
        problem_matrix = cv2.cvtColor(problem_matrix_bgr, cv2.COLOR_BGR2RGB)

        rendered_alternative_list = []
        output_file_obj = None

        if alternatives and alternatives > 1:
            LittleShape.reset_seed()
            LittleShape.set_seed(alternative_seed)
            rendered_alternative_list_bgr, dis_scores = generate_and_save_alternatives(
            matrices, element_types, alternatives, alternative_seed, updated_rules, path, save=False
            )
            rendered_alternative_list = [
            cv2.cvtColor(alt_bgr, cv2.COLOR_BGR2RGB) for alt_bgr in rendered_alternative_list_bgr
            ]

            if output_file == True:
                output_file_obj = create_output_file(updated_rules, dis_scores, seed, alternative_seed, save, path)
                # Return 4 values
                return solution_matrix, problem_matrix, rendered_alternative_list, output_file_obj

            # Return 3 values: no output file but alternatives exist
            return solution_matrix, problem_matrix, rendered_alternative_list

        # No alternatives, just return 2 values
        return solution_matrix, problem_matrix

    
                                            
     
        
def initialise_matrix(rules, seed_list, element_type=["big-shape"]):
    """creates a random matrix as a starting point"""
    matrix = []
    #for loop in which we iterate of the rows and then the columns
    for r in range(3):
        row = []
        for c in range(3):
            # Check if the rule is an instance of Rule and has the POSITION attribute
            # position attribute refers to position in a grid, if there is a position rule, the element will be placed randomly in one the corners
            if not any(rule.attribute_type == AttributeType.POSITION for rule in rules):
                element, seed_list = create_random_element(seed_list, element_type, element_index=(r, c))  # Default position
            else:
                element, seed_list = create_random_element(seed_list, element_type, element_index=(r, c), position="random")  # Random position
            row.append(element)
        matrix.append(row)
    return matrix


def save_matrices(matrices,  path):
        """save matrices in the output folder"""    
        os.makedirs(path, exist_ok=True)        
        
        solution_matrix = render_matrix(matrices)        
        cv2.imwrite(os.path.join(path, "solution.png"), solution_matrix)    
        
        problem_matrix = render_matrix(matrices,  problem_matrix=True)
        cv2.imwrite(os.path.join(path, "problem_matrix.png"), problem_matrix)
      
    
def generate_and_save_alternatives(matrices, element_types, alternatives, alternative_seed, rules, path, save):
    """generates, renders and saves the alternatives"""
    alternative_seed_list = seed_generator(alternative_seed)#separate seedlist for the alternatives
    
    #generate the alternatives and dissimilarity scores
    generated_alternatives, dis_scores = create_alternatives(matrices, element_types, alternatives, alternative_seed_list, rules)
   
    if save is True:
        for idx, answer in enumerate(generated_alternatives):        
            rendered_alternative = render_element(list(answer.split_back().values()), idx)
            cv2.imwrite(os.path.join(path, f"alternative_{idx}.png"), rendered_alternative)
        return dis_scores
   
    if save is False:
        rendered_alternative_list = []
        for idx, answer in enumerate(generated_alternatives):        
            rendered_alternative = render_element(list(answer.split_back().values()), idx)
            rendered_alternative_list.append(rendered_alternative)
        return rendered_alternative_list, dis_scores



def create_output_file(updated_rules, dis_scores, seed_value, alternative_seed_value, save, path):
    'creates an output file with some additional information'
    def format_rule(rule):
        args = [f"Ruletype.{rule.rule_type.name}", f"AttributeType.{rule.attribute_type.name}"]
        if rule.value is not None:
            val = f"'{rule.value}'" if isinstance(rule.value, str) else rule.value
            args.append(f"value = {val}")
        if rule.direction is not None:
            args.append(f"direction = '{rule.direction}'")
        if rule.arithmetic_layout is not None:
            args.append(f"arithmetic_layout = '{rule.arithmetic_layout}'")
        if rule.excluded is not None:
            args.append(f"excluded = {rule.excluded}")
        return f"        Rule({', '.join(args)}),"

    output_lines = []

    # RULES section
    output_lines.append("RULES")
    output_lines.append("rules = {")
    for key, rules in updated_rules.items():
        output_lines.append(f"    '{key}': [")
        for rule in rules:
            output_lines.append(format_rule(rule))
        output_lines.append("    ],")
    output_lines.append("}\n")

    # SEEDS section
    output_lines.append("SEEDS")
    output_lines.append(f"seed = {seed_value}")
    output_lines.append(f"alternative seed = {alternative_seed_value}\n")

    # ALTERNATIVES section
    output_lines.append("ALTERNATIVES")
    output_lines.append(f"number of alternatives: {len(dis_scores)}")
    if dis_scores:
        output_lines.append("dissimilarity of alternatives:")
        for i, score in enumerate(dis_scores):
            output_lines.append(f"\talternative {i + 1}: {score}")
    else:
        output_lines.append("no alternatives provided")

    result = "\n".join(output_lines)

    if save:
        output_path = os.path.join(path, "output.txt")
        with open(output_path, 'w') as file:
            file.write(result)
    else:
        return result



    
    
   
    