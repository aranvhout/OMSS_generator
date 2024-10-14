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
            
            constrain(matrix,attribute)
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.COLOR: 
            constrain(matrix,attribute)         
            
            
            
           
    return matrix
            
def constrain(matrix, attribute):
    for row in matrix:
        # Dynamically access the attribute (shape, color, size, etc.) based on the 'attribute' enum
        attribute_name = attribute.name.lower()  # Convert enum name to lowercase to match attribute name in Entity
        attribute_value = getattr(row[0], attribute_name)  # Access the attribute dynamically

        print(attribute_name, attribute_value.value)
            
     
            
    return matrix
        
        
    
    
    
    
  
    