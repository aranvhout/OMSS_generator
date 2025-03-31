# main.py
from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE, value = 'Triangle'),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE, value = 'Zero'),
        Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')],
        
    
    
       'Line': [
           Rule(Ruletype.CONSTANT, AttributeType.ANGLE, value = 'ONE_EIGHTY'),
           Rule(Ruletype.ARITHMETIC, AttributeType.LINENUMBER, direction = 'subtraction'),
           Rule(Ruletype.CONSTANT, AttributeType.LINETYPE)
       
       ],
       
            
       
       
       
       'LittleShape': [
   #   Rule(Ruletype.PROGRESSION, AttributeType.SHAPE),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.COLOR),
       
           Rule(Ruletype.FULL_CONSTANT, AttributeType.POSITION),
           Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
           Rule(Ruletype.ARITHMETIC, AttributeType.NUMBER),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value ='medium')]}

  

# Generate matrix

create_matrix(rules, alternatives=0, seed =None, alternative_seed = None, entity_types=['BigShape', 'Line'])


