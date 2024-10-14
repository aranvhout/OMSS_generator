# main.py
from rules import Ruletype, AttributeType
from matrix import create_matrix

# Define the rules for the matrix
rules = [
    (Ruletype.RANDOM, AttributeType.SHAPE),
    (Ruletype.CONSTANT, AttributeType.SIZE),
    (Ruletype.RANDOM, AttributeType.COLOR),
    (Ruletype.CONSTANT, AttributeType.ANGLE)
]



# Generate matrix

matrix = create_matrix(3, rules)
for row_index, row in enumerate(matrix):
    print(f"\nRow {row_index + 1}:")
    for i, entity in enumerate(row):
        print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")