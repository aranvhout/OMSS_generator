#imports
from .rules import  AttributeType, apply_rules
from .seed import seed_generator
from .entity import create_random_entity

# import matplotlib.pyplot as plt
from .alternatives import create_alternatives
from .render import render_matrix, render_entity
from .configuration import configuration_settings
from .rules import Rule
import os
import cv2
import random
# Function to create a matrix of entities 
def create_matrix( rules, seed=None, alternatives = None, alternative_seed = None, save = True, output_file = False, entity_types=["big-shape"], path ="output"): 
    

    matrices = {}  # dict to store valid matrices  
    # Generate seed list and seed if needed
    if seed  == None:
        seed = random.randint(0, 999999)
        
    seed_list = seed_generator(seed)
    
    if alternative_seed == None:
        alternative_seed = random.randint(0, 999999)
    
    updated_rules, seed_list = configuration_settings (rules, entity_types, seed_list)#adding constrains to the rules, arithmetic layout
    
    for entity_type in entity_types:
        if entity_type not in updated_rules:
            raise ValueError(f"No rules defined for entity type: {entity_type}")
        entity_rules = updated_rules[entity_type]
                
        while entity_type not in matrices:
            
           # Create a starting matrix for the current entity type
            starting_matrix = initialise_matrix(entity_rules, seed_list, entity_type)#note to self. entity type defined in the for-loop 
            # Apply rules to the starting matrix
            matrix, seed_list = apply_rules(starting_matrix, entity_rules, seed_list)   
            
            matrices[entity_type] = matrix  # Save the valid matrix
        
    if save == True :
        save_matrices(matrices, path)
        if alternatives and alternatives > 1:
            dis_scores = generate_and_save_alternatives(matrices, entity_types, alternatives, alternative_seed, updated_rules, path, save =True)
            if output_file == True:
                create_output_file(updated_rules, dis_scores, seed, alternative_seed, save, path)
        print('matrix created')
        
    if save == False:
        solution_matrix_bgr = render_matrix(matrices)
        solution_matrix = cv2.cvtColor(solution_matrix_bgr, cv2.COLOR_BGR2RGB)
        problem_matrix_bgr = render_matrix(matrices, problem_matrix=True)
        problem_matrix = cv2.cvtColor(problem_matrix_bgr, cv2.COLOR_BGR2RGB)
        
        if alternatives and alternatives > 1:
            rendered_alternative_list_bgr, dis_scores = generate_and_save_alternatives(matrices, entity_types, alternatives, alternative_seed, updated_rules, path, save =False)
            rendered_alternative_list = []
            for alternative_bgr in rendered_alternative_list_bgr:
                alternative = cv2.cvtColor(alternative_bgr, cv2.COLOR_BGR2RGB)
                rendered_alternative_list.append(alternative)
            if output_file == True:
                output_file = create_output_file(updated_rules, dis_scores, seed, alternative_seed, save, path)    
        print('matrix created')
        return solution_matrix, problem_matrix, rendered_alternative_list, output_file   
    
    
    
    
                                    
     
        
def initialise_matrix(rules, seed_list=None, entity_type=["big-shape"]):
    matrix = []
    for r in range(3):
        row = []
        for c in range(3):
            # Check if the rule is an instance of Rule and has the POSITION attribute
            if not any(isinstance(rule, Rule) and rule.attribute_type == AttributeType.POSITION for rule in rules):
                entity, seed_list = create_random_entity(seed_list, entity_type, entity_index=(r, c))  # Default position
            else:
                entity, seed_list = create_random_entity(seed_list, entity_type, entity_index=(r, c), position="random")  # Random position
            row.append(entity)
        matrix.append(row)
    return matrix


def save_matrices(matrices,  path):
    
        os.makedirs(path, exist_ok=True)
        
        solution_matrix = render_matrix(matrices)
        
        cv2.imwrite(os.path.join(path, "solution.png"), solution_matrix)
    
        problem_matrix = render_matrix(matrices,  problem_matrix=True)
        cv2.imwrite(os.path.join(path, "problem_matrix.png"), problem_matrix)
      
    
def generate_and_save_alternatives(matrices, entity_types, alternatives, alternative_seed, rules, path, save):
    alternative_seed_list = seed_generator(alternative_seed)
    generated_alternatives, dis_scores = create_alternatives(matrices, entity_types, alternatives, alternative_seed_list, rules)
    if save is True:
        for idx, answer in enumerate(generated_alternatives):        
            rendered_alternative = render_entity(list(answer.split_back().values()), idx)
            cv2.imwrite(os.path.join(path, f"alternative_{idx}.png"), rendered_alternative)
        return dis_scores
    if save is False:
        rendered_alternative_list = []
        for idx, answer in enumerate(generated_alternatives):        
            rendered_alternative = render_entity(list(answer.split_back().values()), idx)
            rendered_alternative_list.append(rendered_alternative)
        return rendered_alternative_list, dis_scores



def create_output_file(updated_rules, dis_scores, seed_value, alternative_seed_value, save, path):
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



    
    
   
    