"""
omss: Open Matrices Stimuli Set

A Python package for generating matrix reasoning puzzles inspired by Raven's Progressive Matrices.
Useful for research on fluid intelligence and procedural visual reasoning tasks.

Main Function:
    create_matrix(
        rules,
        seed=None,
        alternatives=None,
        alternative_seed=None,
        save=True,
        output_file=False,
        entity_types=["big-shape"],
        path=None
    )

Arguments:
    - rules: dict
        Rules that govern entity transformations.
    - seed: int, optional
        Seed for puzzle generation (default: None).
    - alternatives: int, optional
        Number of distractor options (default: None).
    - alternative_seed: int, optional
        Seed for generating alternatives (default: None).
    - save: bool, optional
        Whether to save output as images (default: True).
    - output_file: bool, optional
        Save metadata (solution, rules, etc.) (default: False).
    - entity_types: list
        Which entities to include (e.g., ["BigShape"]).
    - path: str, optional
        Output directory (default: ~/Documents/OMSS_output).

Docs & source:
    https://github.com/aranvhout/OMSS_generator

Example:
    from omss import Rule, Ruletype, AttributeType, create_matrix

    rules = {
        'BigShape': [
            Rule(Ruletype.PROGRESSION, AttributeType.SIZE),
            Rule(Ruletype.CONSTANT, AttributeType.SIZE),
            Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
            Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
            Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value='medium')
        ]
    }

    create_matrix(
        rules,
        alternatives=8,
        entity_types=['BigShape'],
        path="/Users/yourname/Desktop/NewStimuli/"
    )
"""


from .rules import Ruletype, AttributeType, Rule
from .matrix import create_matrix