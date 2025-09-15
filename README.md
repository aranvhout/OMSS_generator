[![PyPi](https://img.shields.io/pypi/v/omss)](https://pypi.org/project/omss/)
<!--- [![Downloads](https://img.shields.io/pypi/dw/omss)](https://pypi.org/project/omss)



<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/omss_logo.png" width="350">

## Open Matrices Stimulus Set (omss)
**omss** is a Python package for generating matrix reasoning puzzles, inspired by Raven's Progressive Matrices. It allows users to generate an unlimited number of customizable puzzles across a range of difficulty levels by setting rules for visual elements. Please check out the [`Documentation`](https://github.com/aranvhout/OMSS_generator/blob/main/tutorial.md) for more information. 


## Features

- Customizable matrix reasoning puzzle generation
- Reproducibility with seed control
- Colorblind-friendly visual design
- 5 different rules: `distribute_three`, `progression`, `arithmetic`, `constant`, `full_constant`
- Generate virtually unlimited unique puzzle variations
- Includes ~80 predefined rulesets across 6 difficulty levels, each of which can produce a huge variety of distinct puzzles

<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/example1.png" width="230">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/example2.png" width="230">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/example3.png" width="230">

  

## Installation 

```bash
pip install omss
```

## Quick start
```{python}
#import statements
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix, plot_matrices, ruleset

#define the rules for the puzzle
rules = {
    'BigShape': [       
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    
#create the matrices and alternatives
solution_matrix, problem_matrix, alternatives = create_matrix(rules, alternatives =4, save = False)

#plot the matrices and alternatives
plot_matrices(solution_matrix, problem_matrix, alternatives)
```

<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/problem_matrix.png" width="260">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/solution.png" width="260">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/alternative_0.png" width="110">&nbsp;
<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/alternative_1.png" width="110">&nbsp;
<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/alternative_2.png" width="110">&nbsp;
<img src="https://raw.githubusercontent.com/aranvhout/OMSS_generator/main/images/alternative_3.png" width="110">&nbsp;


## Documentation
For full examples and advanced usage, see the full tutorial and documentation: [`Tutorial and documentation`](https://github.com/aranvhout/OMSS_generator/blob/main/tutorial.md)

## License
This project is licensed under the terms of the GNU license: [LICENSE](https://github.com/aranvhout/OMSS_generator/blob/main/LICENSE).

## Acknowledgements
This project was funded by the NWO Open Science grant ([OSF23.2.029](https://www.nwo.nl/en/projects/osf232029): *Open Matrices: A global, free resource for testing cognitive ability*) and the [Netherlands eScience Center fellowship](https://www.esciencecenter.nl/news/fellow-feature-nicholas-juud/) of Nicholas Judd.

The package itself was inspired in part by [`raven-gen`](https://github.com/shlomenu/raven-gen).  *Chi Zhang*, *Feng Gao*, *Baoxiong Jia*, *Yixin Zhu*, *Song-Chun Zhu* *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019* 

Aran van Hout, Jordy van Langen, Rogier Kievit, Nicholas Judd
