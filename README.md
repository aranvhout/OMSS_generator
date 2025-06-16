# omss

**omss** is a Python package for generating matrix reasoning puzzles, inspired by Raven's Progressive Matrices, designed to assess fluid intelligence in humans. It allows users to generate an unlimited number of customizable puzzles across a range of difficulty levels. 

The package was inspired in part by [`raven-gen`](https://github.com/shlomenu/raven-gen).  
*Chi Zhang*, *Feng Gao*, *Baoxiong Jia*, *Yixin Zhu*, *Song-Chun Zhu*  
*Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019*  

**omss** has been rebuilt from scratch, with a focus on flexibility, reproducibility, and suitability for human testing.

## Features

- Fully customizable puzzle generation, including ways to manipulate difficulty and combine visual elements
- Believable distractors generated using a tree-based transformation system
- Reproducibility via seed values for both puzzles and distractors
- Colorblind-friendly visual design
- 5 types of Rules

## Installation 

```bash
pip install omss
```

## Example

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.PROGRESSION, AttributeType.SIZE),
        Rule(Ruletype.CONSTANT, AttributeType.SIZE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}


create_matrix(rules, alternatives=8, entity_types=[ 'BigShape'], path = "/Users/njudd/Desktop/NewStimuli/")
