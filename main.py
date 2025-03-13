# main.py
from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE, value = 'Triangle'),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE, value = 'Zero'),
        Rule(Ruletype.ARITHMETIC, direction = 'addition'),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')],
        
    
    
       'Line': [
           Rule(Ruletype.FULL_CONSTANT, AttributeType.ANGLE, value = 'ONE_EIGHTY'),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINENUMBER),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINETYPE)
       
       ],
       
       
       
       
       
       
       'LittleShape': [
   #   Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.COLOR),
       
           Rule(Ruletype.FULL_CONSTANT, AttributeType.POSITION),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE),
          
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  

# Generate matrix

create_matrix(rules, alternatives=0, seed =None, alternative_seed = 2, entity_types=['BigShape', 'Line'])



