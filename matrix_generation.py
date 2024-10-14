from enum import Enum, auto
import random
import numpy as np

from main import rules
# Generate a row of entities with the specified rules
row_entities = create_row(rules)

# Print the generated entities
for i, entity in enumerate(row_entities):
    print(f"Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")
