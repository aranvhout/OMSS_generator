# main.py

from row_generation import create_row
from rules import Ruletype, AttributeType

# Define the rules for the row
rules = [
    (Ruletype.PROGRESSION, AttributeType.SHAPE),
    (Ruletype.CONSTANT, AttributeType.SIZE),
    (Ruletype.RANDOM, AttributeType.COLOR),
    (Ruletype.CONSTANT, AttributeType.ANGLE)
]

# Generate a row of entities with the specified rules
row_entities = create_row(rules)

# Print the generated entities
for i, entity in enumerate(row_entities):
    print(f"Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")
