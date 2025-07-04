
# OMSS documentation

**omss** is a Python package for generating matrix reasoning puzzles, inspired by Raven's Progressive Matrices, designed to assess fluid intelligence. It allows users to generate an unlimited number of customizable puzzles across a range of difficulty levels. 

The package was inspired in part by [`raven-gen`](https://github.com/shlomenu/raven-gen).  
*Chi Zhang*, *Feng Gao*, *Baoxiong Jia*, *Yixin Zhu*, *Song-Chun Zhu*  
*Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019*  

**omss** has been rebuilt from scratch, with a focus on flexibility, reproducibility, and suitability for human testing.

## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Rules and RuleTypes](#ruletypes)
- [Elements and AttributeTypes](#elements-and-attributes)
- [Matrix Generation](#matrix-generation)
- [Alternatives Generation](#alternatives-generation)
- [Seeds](#seeds)
- [Multiple Elements](#multiple-elements)
- [Additional Settings](#Additional-settings)


## Overview

OMSS works with **elements** which a placed in 3 x 3 matrix. These elements have a visual appearance which is determined by their **atributes**. Specific instances of these attributes may change within a row according to a logical pattern. This logical pattern is determined by the user with **Rules**.


### Function Signature

**`create_matrix(rules, alternatives=None, seed=None, alternative_seed=None, save=True, output_file=False, element_types=None, path=None)`**

#### Parameters

- **`rules`** (*required*, `dict`):  
  A dictionary containing both the `RuleType` and the `AttributeType` that each rule applies to.

- **`alternatives`** (`int`, optional):  
  The number of alternatives to generate. Must be between 0 and 32 (up to 64 depending on settings).  
  Default: `None`.

- **`seed`** (`int`, optional):  
  Seed for the main matrix generation. Used for reproducibility.  
  Default: `None`.

- **`alternative_seed`** (`int`, optional):  
  Seed for generating alternatives.  
  Default: `None`.

- **`save`** (`bool`, optional):  
  Whether to save the matrix and alternatives to disk.  
  - `True`: Saves files to the specified path (or a default folder).  
  - `False`: Returns the matrix and alternatives as Python objects.  
  Default: `True`.

- **`output_file`** (`bool`, optional):  
  Whether to generate an extra output file with metadata about the rules, seeds, alternatives.  
  Default: `False`.

- **`element_types`** (`list` or `None`, optional):  
  Specifies which elements to include in the matrix.  
  - If `None`, all elements listed in the `rules` will be used.  
  Default: `None`.

- **`path`** (`str` or `None`, optional):  
  Path where matrices and alternatives will be saved.  
  - If `None` and `save=True`, a folder named `OMSS_output` is created in the user’s Documents directory.  
  Default: `None`.

---


### Example
In the example below, we use the program to define some rule types for the attributes of an element called BigShape. To keep things simple, we'll create a basic puzzle by applying the CONSTANT rule type and using the program's default settings by only specifying the rules.

```python
#import statements
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

#the dictionary for the in which RuleTypes are coupled to AttributeTypes
rules = {
    'BigShape': [       
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    
#the function that creates the matrices
create_matrix(rules)
```

In the following sections, we will first cover the different **rules**, **elements**, and their **attributes**. Next, we’ll explain the process of **matrix generation**, the creation of **alternatives**, how **seeds** function, and finally, some additional **custom settings**.

## Installation









## Rules
Rules are defined by the user and determine how attributes change across columns in the matrix. Each rule is composed of a RuleType and an AttributeType. The RuleType defines the logical pattern of modification, while the AttributeType specifies which attribute is affected.

Most RuleTypes are general and can operate on any AttributeType. However, each AttributeType can be governed by only one RuleType.

Since RuleTypes are general and shared across elements, they are discussed here. AttributeTypes, on the other hand, are specific to each element and will be addressed in the Elements section.



### RuleTypes
OMSS uses 5 different RuleTypes, namely: constant, full_constant, distribute_three, progression and arithmetic

#### **CONSTANT**
The `CONSTANT` rule ensures that an attribute remains unchanged **within a row**.  
For example, if a `color` attribute is governed by the `CONSTANT` rule, all elements in the same row will have the same color.

---
####  Example
Let’s create a very straightforward matrix puzzle. We'll once again use the BigShape element and set all of its AttributeTypes to CONSTANT, ensuring that no attribute changes within any row. This creates a simple, uniform pattern and serves as a good starting point for understanding how rule definitions work.


```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.CONSTANT, AttributeType.SIZE)}
    

create_matrix(rules)
```


#### **FULL_CONSTANT**
The `FULL_CONSTANT` rule ensures that an attribute remains unchanged **across the entire matrix**. It is also possible to specify the specific value of the unchanged attribute.

#### Example
Let’s simplify the previous example even further by applying the FULL_CONSTANT rule to the color attribute. This means that all elements in the matrix will now have the same color, as opposed to the previous case where colors were constant only within rows.

To further enhance the uniformity of the matrix, we'll also apply the FULL_CONSTANT rule to the size attribute and fix it to a preselected value. The available size values are 'small', 'medium', and 'large'.

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')}
    

create_matrix(rules)
```
---

#### **DISTRIBUTE_THREE**
The `DISTRIBUTE_THREE` rule distributes **three distinct values** of an attribute across each row.  
For example, if the `shape` attribute uses this rule, each row will contain the same three different shapes (e.g., triangle, square, circle).

#### Example
Until now, our puzzles have been fairly lackluster. By applying the `DISTRIBUTE_THREE` rule, we can start creating puzzles with actual variation and a more complicated logical structure.

Let’s enhance the previous matrix by applying the `DISTRIBUTE_THREE` rule to the color attribute. This means each row will now contain three different colors, adding a more interesting pattern for the solver to detect.

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

print(1+1)
rules = {
    'BigShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.CONSTANT, AttributeType.SIZE, value = 'medium')}
    

create_matrix(rules)
```

It’s also possible to apply multiple `DISTRIBUTE_THREE` rules to different attribute types within a single matrix. Building on the previous example, we now apply a `DISTRIBUTE_THREE` rule to both the shape and color attributes. This creates an even more varied and engaging puzzle by distributing three distinct shapes and three distinct colors across each row.

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULLCONSTANT, AttributeType.SIZE, value = 'medium')}
    

create_matrix(rules)
```

---

#### **PROGRESSION**
The PROGRESSION rule increases or decreases the value of an attribute across a row.
For example, when applied to the size attribute, element sizes will progressively grow or shrink within each row.

Attributes are represented by classes that have a defined order. The PROGRESSION rule follows this order to modify attribute values step-by-step. For instance, the shape attribute is ordered from simpler to more complex shapes, allowing the rule to create a logical progression.

`PROGRESSION` can be also applied to less intuitive attributes, even colour; however, doing so will produces less intuitive or meaningful results.

---
#### Example
To properly showcase the `PROGRESSION` rule we will introduce a new type of `element`, namely `LittleShape`. `LittleShape` is quite similar to `BigShape` in terms of its attributes and appearance, but it is a bit smaller. As a consequence, it is possible to fit multiple `LittleShape` elements a single grid.

Below we will apply a `PROGRESSION` rule to `LittleShape`'s number attribute! As you can see the number of elements increases/decreases 

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'LittleShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.CONSTANT, AttributeType.COLOR),
        Rule(Ruletype.PROGRESSION, AttributeType.LITTLESHAPENUMBER),
        Rule(Ruletype.FULLCONSTANT, AttributeType.SIZE, value = 'medium')}
    

create_matrix(rules)
```

#### **ARITHMETIC**
The `ARITHMETIC` rule performs **addition or subtraction operations**, and can only be applied to numeric attributes.  If multiple element types share this rule, their attribute values will be added to or subtracted from one another.

---
### Examples
Let's revisit the earlier matrix example and see if we can produce a more interesting puzzle. Previously, all rules were set to constant or full_constant. If we change the Ruletype for the color attributeType to `DISTRIBUTE_THREE` the puzzle already becomes more interesting.

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    

create_matrix(rules)
```
There are now three colours distributed over the elements in a row. As mentioned before, each Rule can be applied to multiple attributesLet's further complicate the puzzle by also setting a `DISTRIBUTE_THREE` for shape.

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    

create_matrix(rules)
```

Now, let's play around with the `FULL_CONSTANT` rule by setting shape to `FULL_CONSTANT`. 

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE, value = 'medium')]}
    

create_matrix(rules)
```
The same shape is now distributed across the entire matrix. Contrast this to the `CONSTANT` rule in which the shapes still differed within the matrix. It is also possible to specify the attribute instance of the `

Finally, we apply the `PROGRESSION` rule to size. 

```python
import omss
from omss import Ruletype, AttributeType, Rule, create_matrix

rules = {
    'BigShape': [       
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE),
        Rule(Ruletype.CONSTANT, AttributeType.ANGLE),
        Rule(Ruletype.DISTRIBUTE_THREE, AttributeType.COLOR),
        Rule(Ruletype.CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.PROGRESSION, AttributeType.SIZE,]}
    

create_matrix(rules)
```
As you

