# OMMS_generator
### Current to do list
- create all the rules
- add render module
- alternatives

### Broader picture/horizons
- add binding rule (and checks for it)
- create more complicated configurations (allowing new rules such as arithmetic and position) (note to self, probably easiest to adjust current 2-d matrices to the 3-d ones, with the z-axis referring to the addinational entities in a cell)

### Non-urgent to do list:
- Update get_random_attribute function name, it is now more generalised
-  improve  matrix handling. Now if a matrix attribute accidently follows a rule, a totally new matrix is created. It would make more sense to only change the attribute that follows the rule. Would need to create new function for that
-  related to the above: currently the programm will work like this:
-  1) create random matrix
   2) apply rules
   3) check accidental rules
   4) possibly recreate the random matrix in case of 3
   however if would be better if 2 and 3 are reversed. NOTE( not 100 sure whether this is true, potentially applying the rules might create new rules, although I am almost 100 percent sure this is not true. Need to consider it
- Progression rules work, but might be nice to prevent the same attributes appearing in each row (which essentialy is also a distribute three rule)
 
