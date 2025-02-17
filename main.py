# main.py
from rules import Ruletype, AttributeType, Rule
from matrix import create_matrix




# Define rules for each entity
rules = {
    'BigShape': [
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE, value = 'Circle'),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.PROGRESSION, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.SIZE)],
    
    
       'Line': [
           Rule(Ruletype.FULL_CONSTANT, AttributeType.ANGLE, value = 'ONE_EIGHTY'),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINENUMBER),
           Rule(Ruletype.RANDOM, AttributeType.LINELENGTH, value = 'LONG'),
           Rule(Ruletype.RANDOM, AttributeType.LINEWIDTH, value = 'MEDIUM'),
           Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium'),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.LINETYPE),
           Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.POSITION),
       
       ]}



# Generate matrix

matrix = create_matrix(3, 3, rules, alternatives=16, seed = None, entity_types=['BigShape'])
# Attribute mapping for each entity type
entity_attributes = {
    "big-shape": ["shape", "size", "color", "angle", "position", "index"],
    "line": ["color", "linetype", "linewidth", "position" ,"index"]
}

# Check and print the matrix for the specified entity type
a = True
entity_type = "big-shape"  # Specify the entity type to print

if a is True and entity_type in matrix:
    matrix = matrix[entity_type]  # Retrieve the matrix for the specified entity type
    
    # Get the attributes for the current entity type
    attributes = entity_attributes.get(entity_type, [])
    
    for row_index, row in enumerate(matrix):
        print(f"\nRow {row_index + 1}:")
        for i, entity in enumerate(row):
            # Dynamically build the print statement
            entity_details = ", ".join(
                f"{attr.capitalize()}={getattr(entity, attr, 'N/A')}" for attr in attributes
            )
            print(f"  Entity {i + 1}: {entity_details}")
else:
    print(f"Matrix for entity type '{entity_type}' not found or 'a' is False.")

            
