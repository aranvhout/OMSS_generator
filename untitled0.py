# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 10:34:38 2024

@author: Work
"""
import random
a=[]
choices=[5,1,2,3,4,5,6,7,8]
for i in range(2):
    random.seed(a[0])
    attribute = random.sample(choices)
    print(attribute)