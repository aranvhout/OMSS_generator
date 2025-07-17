# omss

**omss** is a Python package for generating matrix reasoning puzzles, inspired by Raven's Progressive Matrices, designed to assess fluid intelligence. It allows users to generate an unlimited number of customizable puzzles across a range of difficulty levels. 


## Features

- Customizable matrix reasoning puzzle generation
- Adjustable difficulty via rule-based system
- Tree-based distractor generation
- Reproducibility with seed control
- Colorblind-friendly visual design
- 5 rule types: `constant`, `full_constant`, `distribute_three`, `progression`, `arithmetic`


## Explanation of the github
- license
- tutorial/documentation

## Installation 

```bash
pip install omss
```

## Quick start
```{python}
#import statements
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix, plot_matrices

#the dictionary for the in which RuleTypes are coupled to AttributeTypes
rules = {
    'BigShape': [       
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    
#create the matrices
solution_matrix, problem_matrix = create_matrix(rules, save = False)

#plot the matrices
plot_matrices(solution_matrix, problem_matrix)

#save the matrices
#
```

## Documentation
For full examples and advanced usage, see the full tutorial and documentation: [`Tutorial and documentation`](https://github.com/aranvhout/OMSS_generator/blob/main/How%20to%20get%20started%20with%20omss.md)

## License
This project is licensed under the terms of the GNU license: ['LICENSE'](https://github.com/aranvhout/OMSS_generator/blob/main/LICENSE).

## Acknowledgements
This project was funded by the NWO Open Science grant ([OSF23.2.029](https://www.nwo.nl/en/projects/osf232029): *Open Matrices: A global, free resource for testing cognitive ability*) and the [Netherlands eScience Center fellowship](https://www.esciencecenter.nl/news/fellow-feature-nicholas-juud/) of Nicholas Judd.

The package itself was inspired in part by [`raven-gen`](https://github.com/shlomenu/raven-gen).  *Chi Zhang*, *Feng Gao*, *Baoxiong Jia*, *Yixin Zhu*, *Song-Chun Zhu* *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019* 

Aran van Hout, Jordy van Langen, Rogier Kievit, Nicholas Judd
