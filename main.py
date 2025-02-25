# main.py
from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.PROGRESSION, AttributeType.ANGLE),
       
        Rule(Ruletype.CONSTANT, AttributeType.SIZE)],
    
    
       'Line': [
           Rule(Ruletype.FULL_CONSTANT, AttributeType.ANGLE, value = 'ZERO'),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINENUMBER),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.LINELENGTH, value = 'LONG'),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.LINEWIDTH, value = 'MEDIUM'),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium'),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.LINETYPE),
       ],
       
       
       
       
       'LittleShape': [
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.SHAPE),
           Rule(Ruletype.CONSTANT, AttributeType.COLOR, value = 'lavender'),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.ANGLE),
           Rule(Ruletype.PROGRESSION, AttributeType.POSITION),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  

# Generate matrix

matrix = create_matrix(rules, alternatives=8, seed = None, alternative_seed = None, entity_types=['BigShape', 'LittleShape'])


            
