
# OMSS documentation

**omss** is a Python package for generating matrix reasoning puzzles, inspired by Raven's Progressive Matrices, designed to assess fluid intelligence. It allows users to generate an unlimited number of customizable puzzles across a range of difficulty levels. 

The package was inspired in part by [`raven-gen`](https://github.com/shlomenu/raven-gen).  
*Chi Zhang*, *Feng Gao*, *Baoxiong Jia*, *Yixin Zhu*, *Song-Chun Zhu*  
*Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019*  

**omss** has been rebuilt from scratch, with a focus on flexibility, reproducibility, and suitability for human testing.

## Contents

- [Overview](#overview)
- [Rules and RuleTypes](#ruletypes)
- [Elements and Attributes](#elements-and-attributes)
- [Matrix Generation](#matrix-generation)
- [Alternatives Generation](#alternatives-generation)
- [Seeds](#seeds)
- [Multiple Elements](#multiple-elements)
- [Additional Settings](#Additional-settings)


## Overview

OMSS works with **elements** which a placed in 3 x 3 matrix. These elements have a visual appearance which is determined by their **atributes**. Specific instances of these attributes may change within a row according to a logical pattern. This logical pattern is determined by the user with **Rules**. Importantly, each **attribute** is always goverened by only one **RuleType**. 

### Example
In the the code below we will set some ruletypes for the attributes of an element called 'BigShape'. BigShape has a number of attributes (angle, shape, color, size, number). Each of these attributes can take on multiple instances. For example, the color attribute determines the color of the shape and has 8 colors (). 

For now we will create a simple puzzle by using Constant ruletype which ensure that the attributes do not change within a row.

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

## Rules and Ruletypes
Rules are defined by the user and govern how attributes change across columns. Each rule consists of a RuleType and an AttributeType object. The RuleType defines the logical pattern by which an attribute is modified, while the AttributeType specifies which attribute the rule affects. Consequently, each AttributeType is modified by exactly one RuleType. Moreover, most RuleTypes can operate on all AttributeTypes. 

For the sake of simplicity, we will refer to RuleTypes simply as rules, and to AttributeTypes as attributes from this point onward.

OMSS uses 5 rules:

#### **CONSTANT**
The `CONSTANT` rule ensures that an attribute remains unchanged **within a row**.  
For example, if a `color` attribute is governed by the `CONSTANT` rule, all elements in the same row will have the same color.

---

#### **FULL_CONSTANT**
The `FULL_CONSTANT` rule ensures that an attribute remains unchanged **across the entire matrix**.  
For instance, if a `color` attribute is governed by the `FULL_CONSTANT` rule, every element in the matrix will share the same color.

---

#### **DISTRIBUTE_THREE**
The `DISTRIBUTE_THREE` rule distributes **three distinct values** of an attribute across each row.  
For example, if the `shape` attribute uses this rule, each row will contain the same three different shapes (e.g., triangle, square, circle).

---

#### **PROGRESSION**
The `PROGRESSION` rule increases or decreases the value of an attribute across a row.  
For instance, if applied to the `size` attribute, element sizes will progressively grow or shrink within a row.

This rule can also be applied to less intuitive attributes like `shape` (e.g., from simple to complex forms) or even `color`—though the latter is **discouraged**, as it tends to produce inconsistent or meaningless results.

---

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

