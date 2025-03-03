# main.py
from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.SHAPE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium'),
      ],
    
    
       'Line': [
           Rule(Ruletype.FULL_CONSTANT, AttributeType.ANGLE, value ='zero'),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINENUMBER),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.LINELENGTH, value = 'Long'),
           Rule(Ruletype.CONSTANT, AttributeType.LINEWIDTH),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE),
           Rule(Ruletype.CONSTANT, AttributeType.LINETYPE),
       ],
       
       
       
       
       'LittleShape': [
   #   Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.COLOR),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.ANGLE),
           Rule(Ruletype.PROGRESSION, AttributeType.POSITION),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  

# Generate matrix

create_matrix(rules, alternatives=4, seed = None, alternative_seed = 4, entity_types=[ 'BigShape'])



