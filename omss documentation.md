
# OMSS documentation

**omss** is a Python package for generating matrix reasoning puzzles, inspired by Raven's Progressive Matrices, designed to assess fluid intelligence. It allows users to generate an unlimited number of customizable puzzles across a range of difficulty levels. 

The package was inspired in part by [`raven-gen`](https://github.com/shlomenu/raven-gen).  
*Chi Zhang*, *Feng Gao*, *Baoxiong Jia*, *Yixin Zhu*, *Song-Chun Zhu*  
*Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019*  

**omss** has been rebuilt from scratch, with a focus on flexibility, reproducibility, and suitability for human testing.

## Contents

- [Overview](#overview)
- [Rules](#rules)
- [Elements and Attributes](#elements-and-attributes)
- [Matrix Generation](#matrix-generation)
- [Alternatives Generation](#alternatives-generation)
- [Seeds](#seeds)
- [Multiple Elements](#multiple-elements)
- [Custom Settings](#custom-settings)


## Overview

OMSS works with **elements**, these elements have a visual appearance which is determined by their **atributes**. Specific instances of these attributes may change within a row according to a logical pattern. This logical pattern is determined by the user with **Rules**. Importantly, each **attribute** is always goverened by only one **Rule**. 

### Example
In the the code below we will set some rules for the attributes of an element called 'BigShape'. BigShape has a number of attributes (angle, shape, color, size, number). Each of these attributes can take on multiple instances. For example, the color attribute determines the color of the shape and has 8 colors (). 

For now we will create a simple puzzle by using Constant rule which ensure that the attributes do not change within a row.

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    

create_matrix(rules)
```
In the following sections, we will first cover the different **rules**, **elements**, and their **attributes**. Next, we’ll explain the process of **matrix generation**, the creation of **alternatives**, how **seeds** function, and finally, some additional **custom settings**.

