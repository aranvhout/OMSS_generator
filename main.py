# main.py
# a minimal example of the generator

# files needed: matrix.py, render.py, alternatives.py, rules.py, configuration.py, entities

from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix
import matplotlib.pyplot as plt
from PIL import Image


# Simple example, everything constant but progressing angle
r1 = {
    'BigShape': [
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE, value = 'square'),
        Rule(Ruletype.PROGRESSION, AttributeType.ANGLE),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.COLOR, value = 'blue'),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE)]}


solution_matrix, problem_matrix, alternatives = create_matrix(r1, alternatives=4, seed = None,  alternative_seed =None ,save = False, entity_types=[ 'BigShape',])


# solution_matrix is a bit map

plt.imshow(Image.fromarray(solution_matrix), cmap='gray')
plt.axis('off')
plt.show()




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE, value = 'square'),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR, value = 'red'),
        Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER),
        Rule(Ruletype.CONSTANT, AttributeType.SIZE)],

       'Line': [
           Rule(Ruletype.CONSTANT, AttributeType.ANGLE, value = 'ONE_EIGHTY'),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINENUMBER),
           Rule(Ruletype.CONSTANT, AttributeType.LINETYPE)
       
       ],

       'LittleShape': [
   #   Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
           Rule(Ruletype.CONSTANT, AttributeType.COLOR),
       
           Rule(Ruletype.CONSTANT, AttributeType.POSITION),
           Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
           Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  

# Generate matrix

#solution_matrix, problem_matrix, alternatives = create_matrix(rules, alternatives=4, seed = None,  alternative_seed =None ,save =False, entity_types=[ 'BigShape','LittleShape', 'Line', ])

#12345788912457
#111245511123,