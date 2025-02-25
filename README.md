# OMMS_generator
### Current to do list
- create all the rules Fixed!!
- add subentities (see below)
- add render module Fixed!!
- fix the misbehaving rules (eg with distribute three the circles are always red) Fixed!!
- alternatives X
- position for line entity (middle (big), and all the corners). Rules so be able to change this (progression, distribute three, random, constant). But also the user should be able to put the stimuli in the main center square 
  best way would be to add a placement rule. if the spefified middle, the entity would just be placed there. other rule that apply to the position should disregard the middle option i think
### Subentities
I think these subentities can be best viewed as an separate class from the main entities (aka shapes). The program should first create matrix for the normal entities, makes sure everything works and only then go for these subentities. You can almost think of it as a seperate puzzle from the main entities

### Broader picture/horizons
- add binding rule (and checks for it)
- create more complicated configurations (allowing new rules such as arithmetic and position) (note to self, probably easiest to adjust current 2-d matrices to the 3-d ones, with the z-axis referring to the addinational entities in a cell)
- instead of the above, I could also opt for add-ons on top of the shapes (like three crossed lines etc). This would be a lot easier to code I reckon and resembles the original raven matrices a bit better

### Non-urgent to do list:
- Update get_random_attribute function name, it is now more generalised
-  improve  matrix handling. Now if a matrix attribute accidently follows a rule, a totally new matrix is created. It would make more sense to only change the attribute that follows the rule. Would need to create new function for that
-  related to the above: currently the programm will work like this:
-  1) create random matrix
   2) apply rules
   3) check accidental rules
   4) possibly recreate the random matrix in case of 3
   however if would be better if 2 and 3 are reversed. NOTE( not 100 sure whether this is true, potentially applying the rules might create new rules, although I am almost 100 percent sure this is not true. Need to consider it
- Have a constrain option. Now, the matrices might look weird and ugly since just by chance a distribute three rule might look like a progression etc etc. (I know what I mean by this),
also for example with the random rule, just by chance a colour might be really dominant
- remove columns and row arguments
 - what if not all the rules are specified for an entity. I think it just fills in random stuff, but doesnt check whether there are accidental patterns. maybe make constant the default
 
 -make sure a seed_list is returned in more functions!!
 -HOW DOES FULL CONSTANT RELATE TO ALTERNATIVES? SOLVED, just put it back at the splitting order
 -constant should always have different values for each row, FIXED