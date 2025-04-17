# main.py
from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE, value = 'square'),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER, direction = 'subtraction'),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')],
        
    
    
       'Line': [
           Rule(Ruletype.CONSTANT, AttributeType.ANGLE, value = 'ONE_EIGHTY'),
           Rule(Ruletype.ARITHMETIC, AttributeType.LINENUMBER),
           Rule(Ruletype.CONSTANT, AttributeType.LINETYPE)
       
       ],
       
            
       
       
       
       'LittleShape': [
   #   Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
           Rule(Ruletype.CONSTANT, AttributeType.COLOR),
       
           Rule(Ruletype.CONSTANT, AttributeType.POSITION),
           Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
           Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER, direction = 'subtraction'),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  

# Generate matrix

create_matrix(rules, alternatives=16, seed =12345788912457, alternative_seed =1 , entity_types=['BigShape', 'LittleShape'])


