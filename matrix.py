from enum import Enum, auto
import random
import numpy as np
from row_generation import create_row
from rules import Ruletype, AttributeType


def create_matrix(num_rows, rules):
    matrix = []
    
    # Generate rows based on rules
    for _ in range(num_rows):
        row = create_row (rules)  # Generate a row of entities
        matrix.append(row)       # Add the row to the matrix
    
    # apply constraints
    matrix = constrain_matrix(matrix, rules)  
    return matrix

def constrain_matrix(matrix, rules):    
    for rule, attribute in rules:
        if rule is Ruletype.RANDOM and attribute is AttributeType.SHAPE:             
            constrain(matrix,attribute, rules)#I'm passing rules in order to be able to remake the matrix
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.SIZE:             
            constrain(matrix,attribute, rules)
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.COLOR: 
            constrain(matrix,attribute, rules)         
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.ANGLE: 
            constrain(matrix,attribute, rules) 
            
                      
    return matrix
            
def constrain(matrix, attribute, rules): 
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
   
    # 2 Perform the checks
    #Constant rule  
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
    distribute_three =  True
    reference_row=numerical_matrix[0]    
    for row in numerical_matrix[1:]: 
        if not all(value in reference_row for value in row):  # Check if all values in `row` exist in `reference_row`
            distribute_three = False
            break  # Exit the loop if a value is missing       
    
    #check distribute two (not sure whether to include this yet)
    distribute_two = True   
    common_elements = set(numerical_matrix[0])  # Initialize with the first row
    for row in numerical_matrix[1:]:
        common_elements.intersection_update(row)  # neved heard of this method but it is exactly what we need
    if len(common_elements) <2:
        distribute_two = False

    if constant or upward_progression or downward_progression or distribute_three or distribute_two:
        
        print('recreating matrix', constant, upward_progression, downward_progression, distribute_three, distribute_two)
        for row_index, row in enumerate(matrix):
            print(f"\nRow {row_index + 1}:")
            for i, entity in enumerate(row):
                print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")
        return create_matrix(len(matrix), rules)# for now we just rerun it, I should include a max to ensure we dont get stuck in a loop
    
    else:        
        return matrix
        
        
    
    
    
    
  
    