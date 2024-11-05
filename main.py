# main.py
from rules import Ruletype, AttributeType
from subentities import SubEntityRuletype, Line, SubShape
from matrix import create_matrix

# Define the rules for the matrix
rules = [
    (Ruletype.RANDOM, AttributeType.SHAPE),
    (Ruletype.RANDOM, AttributeType.SIZE),
    (Ruletype.RANDOM, AttributeType.COLOR),
    (Ruletype.RANDOM, AttributeType.ANGLE),
    (SubEntityRuletype.CONSTANT, SubShape.Colors)                                        ]



# Generate matrix
for i in range (0,999):
    matrix = create_matrix(3, rules, i)
    print(i)

a =  False
if a is True:
    for row_index, row in enumerate(matrix):
        print(f"\nRow {row_index + 1}:")
        for i, entity in enumerate(row):
            print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")
            
            