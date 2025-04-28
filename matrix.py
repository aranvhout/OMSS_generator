#imports
from rules import  AttributeType, apply_rules
from seed import seed_generator
from entity import create_random_entity

import matplotlib.pyplot as plt
from alternatives import create_alternatives
from render import render_matrix, render_entity
from configuration import configuration_settings
from rules import Rule
import os
import cv2

# Function to create a matrix of entities 
def create_matrix( rules, seed=None, alternatives = None, alternative_seed = None, save = True,  entity_types=["big-shape"], path ="output"): 
    

    matrices = {}  # dict to store valid matrices  
    seed_list = seed_generator(seed) # Generate seed list
    
    updated_rules, seed_list = configuration_settings (rules, entity_types, seed_list)#adding constrains to the rules, arithmetic layout
    
    for entity_type in entity_types:
        if entity_type not in updated_rules:
            raise ValueError(f"No rules defined for entity type: {entity_type}")
        entity_rules = updated_rules[entity_type]
                
        while entity_type not in matrices:
            
           # Create a starting matrix for the current entity type
            starting_matrix = initialise_matrix(entity_rules, seed_list, entity_type)#note to self. entity type defined in the for-loop 
            # Apply rules to the starting matrix
            matrix = apply_rules(starting_matrix, entity_rules, seed_list)                       
            matrices[entity_type] = matrix  # Save the valid matrix
            
    if save == True :
        save_matrices(matrices, path)
        if alternatives and alternatives > 1:
            generate_and_save_alternatives(matrices, entity_types, alternatives, alternative_seed, updated_rules, path)
    
    if save == False:
        solution_matrix = render_matrix(matrices)
        problem_matrix = render_matrix(matrices, problem_matrix=True)
        return solution_matrix, problem_matrix    
    
    
    
    print('matrix created')
                                    
     
        
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
      
    
def generate_and_save_alternatives(matrices, entity_types, alternatives, alternative_seed, rules, path):
    alternative_seed_list = seed_generator(alternative_seed)
    generated_alternatives = create_alternatives(matrices, entity_types, alternatives, alternative_seed_list, rules)
    for idx, answer in enumerate(generated_alternatives):        
        rendered_alternative = render_entity(list(answer.split_back().values()), idx)
        cv2.imwrite(os.path.join(path, f"alternative_{idx}.png"), rendered_alternative)
        plt.show()




  
    