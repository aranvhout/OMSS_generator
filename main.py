# -*- coding: utf-8 -*-
"""
Created on Mon May 19 15:37:42 2025

@author: Work
"""
#in order to see changes in src reflected in main directly, run the following command in the directory that contaisn the src folder and the pyproject.toml
#pip install -e .
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

import time

start = time.time()

#normal code
rules = {
    'BigShape': [
       
        Rule(Ruletype.PROGRESSION, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')],

       'Line': [
           Rule(Ruletype.PROGRESSION, AttributeType.ANGLE, value = 'ONE_EIGHTY'),
           Rule(Ruletype.ARITHMETIC, AttributeType.LINENUMBER),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINETYPE)
       
       ],

       'LittleShape': [
   #   Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
           Rule(Ruletype.CONSTANT, AttributeType.POSITION),
           Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
           Rule(Ruletype.CONSTANT, AttributeType.COLOR),
           Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
           Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  
#image.save("color_bitmap_output.png")
for i in range (0,1):

 create_matrix(rules, alternatives=16, seed =None,  alternative_seed =None ,save =True, output_file = True, entity_types=[ 'Line'])

 
end = time.time()

print(f"Execution time: {end - start:.4f} seconds")

#bitmap thing
#solution_matrix, problem_matrix, alternatives = create_matrix(rules, alternatives=4, seed = 13,  alternative_seed =None ,save =False, entity_types=[ 'BigShape', 'LittleShape' ])
#array = np.array(solution_matrix, dtype=np.uint8)
#image = Image.fromarray(array, mode='RGB')
#image.save("solution_matrix.png")