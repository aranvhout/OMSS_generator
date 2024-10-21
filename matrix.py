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
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.SIZE:             
            constrain(matrix,attribute)
            
        if rule is Ruletype.RANDOM and attribute is AttributeType.COLOR: 
            constrain(matrix,attribute)         
            
            
            
           
    return matrix
            
def constrain(matrix, attribute): 
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
            break  # No need to check further, set to True and exit
               
     # Check upward progression
    upward_progression = True
    for row in numerical_matrix:
        for i in range(len(row) - 1):  # Loop through indices of the row
            if row[i] >= row[i + 1]:  # Check for strictly increasing
                upward_progression = False
                break  # Exit the inner loop if not progressing
        if not upward_progression:
            break  # Exit the outer loop if a non-progressing row is found
    if upward_progression:
        print('row has been found upward')
        
     # Check downward progression       
    downward_progression = True
    for row in numerical_matrix:
        for i in range(len(row) - 1):  # Loop through indices of the row
            if row[i] <= row[i + 1]:  # Check for strictly decreasing
                downward_progression = False
                break  # Exit the inner loop if not progressing
        if not downward_progression:
            break  # Exit the outer loop if a non-progressing row is found
    if downward_progression:
       print('row has been found downward')    
       

       
#check downward progression
       
    
    
    #check distribute three
    
    
    
    #check distribute two
    
    
    
    
    
    
    
    
  
    return matrix
        
        
    
    
    
    
  
    