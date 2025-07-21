#OMSS imports
from .seed import random_choice
from .rules import Ruletype, Rule

def configuration_settings(rules, element_types, seed_list):
       
    updated_rules = {}

    for element, rule_list in rules.items():
        if element in element_types:  
            updated_rules[element] = []
        
            for rule in rule_list:
            # Create a new Rule instance with all missing attributes set to None
                new_rule = Rule(
                    rule_type=rule.rule_type,
                    attribute_type=rule.attribute_type if rule.attribute_type else None,
                    value=rule.value if rule.value else None,
                    direction=rule.direction if rule.direction else None,
                    arithmetic_layout=rule.arithmetic_layout if rule.arithmetic_layout else None,
                    excluded=rule.excluded if rule.excluded else None
                    )
                updated_rules[element].append(new_rule)

    #constrain function
    if len(element_types)>1: #aka multiple elements
        updated_rules, seed_list = constrain (updated_rules, seed_list) #add constraining settings (potentially)
        


    #check whether we need so set an arithmetic layout    
    has_arithmetic_rule = any(
    any(isinstance(rule, Rule) and rule.rule_type == Ruletype.ARITHMETIC for rule in rule_list)
    for rule_list in updated_rules.values()
)

    if  has_arithmetic_rule is True:
        updated_rules, seed_list = arithmetic_parameters (updated_rules, seed_list)



    return updated_rules, seed_list


def constrain (updated_rules, seed_list):#placeholder for if we want to add constraining possibilities in the future
    return updated_rules, seed_list  
    
 
    
    
def arithmetic_parameters(all_rules, seed_list):
        
    # step 1: categorize elements to do some basic checks    
    SNE_CON, MNE_CON, MNE_NCON, NA_en, All_E = categorize_elements(all_rules)
    
    # step 2: select the direction (subtraction, addition) and layout for the elements 
    all_rules, seed_list = select_direction(SNE_CON, MNE_CON, MNE_NCON, all_rules, seed_list)
                    
    # step 3: assign layouts to single-number elements (for the multiple number elements this is way less of a haz)
    all_rules, seed_list = assign_layouts(all_rules, SNE_CON, MNE_CON, All_E,  seed_list)
    
   
    
    return all_rules, seed_list

def categorize_elements(all_rules):
    NA_en = [] #non aritmetic elements
    SNE_CON = [] #single number elements, all rules constant
    SNE_NCON = [] #sinlge number elements, non constant rules
    MNE_CON = [] #multiple numer elements, all rules constant
    MNE_NCON = [] #mulriple number elements, non constant rules
    
    MNE_list = ['line', 'littleshape']  # define multiple number elements
    
    for element, element_rules in all_rules.items():
        rule_types = []
        has_arithmetic = False
        is_MNE = element.lower() in MNE_list
        rules_constant = False
        for rule_obj in element_rules:
            if isinstance(rule_obj, Rule):
                rule_types.append(rule_obj.rule_type)
                #in case of arithmetic
                if rule_obj.rule_type == Ruletype.ARITHMETIC:
                    has_arithmetic = True            
        if all(rt in {Ruletype.FULL_CONSTANT, Ruletype.CONSTANT, Ruletype.ARITHMETIC} for rt in rule_types):
            rules_constant = True
                   
    
        if has_arithmetic and is_MNE and rules_constant:
            MNE_CON.append (element)
        
        elif has_arithmetic and is_MNE and not rules_constant:
            MNE_NCON.append (element)
            
        elif has_arithmetic and not is_MNE and  rules_constant:
            SNE_CON.append (element)
    
        elif has_arithmetic and not is_MNE and not rules_constant:
            SNE_NCON.append (element)#
            raise ValueError ('All rules should be set to either constant or full constant for an arimethic operation on an element with only two number options (1 or 0)')
            
        else:
            NA_en.append (element)
            
    All_E =  SNE_CON + MNE_CON + MNE_NCON + NA_en        
    if len(SNE_CON) ==1 and len(All_E) ==1:
        raise ValueError ('Not enough elements to perform an arithmetic operation')
    return (SNE_CON, MNE_CON, MNE_NCON, NA_en, All_E)
    
def select_direction (SNE_CON, MNE_CON, MNE_NCON, all_rules, seed_list):
    #combine valid aritmetic elements in a single list:
    A_E = SNE_CON + MNE_CON  + MNE_NCON
    MNE = MNE_CON + MNE_NCON
    
    #select directions
    # step 1; check whether any direction has been specified
    A_E_direction = set ()
    SNE_CON_direction = set ()
    MNE_direction= set ()
    
    for element in A_E:    
        
        for rule in all_rules[element]:
            if isinstance(rule, Rule):
                if rule.rule_type == Ruletype.ARITHMETIC:
                    direction = rule.direction
                    if direction:  # if a direction is specified
                        if direction not in {"addition", "subtraction"}:
                            raise ValueError(f"Invalid direction '{direction}' for element '{element}'. Must be 'addition' or 'subtraction'.")
                        elif element in SNE_CON:
                            SNE_CON_direction.add(direction)
                            A_E_direction.add(direction)
                        elif element in MNE_CON or element in MNE_NCON:
                            MNE_direction.add(direction)
                            A_E_direction.add(direction)
                    
    if len(A_E_direction) == 1: #only direction specified, lets use that one for all elements
        direction = next(iter(A_E_direction))
        set_direction(A_E, all_rules, direction)
        
    elif len (A_E_direction) == 0: #not a single direction specified, lets select one for all elements
        direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
        set_direction(A_E, all_rules, direction)
        
    elif len (A_E_direction) > 1 :#multiple directions specified, lets investigate    
        if len(SNE_CON)>0: #if we have single numebr elements
            
            if len(SNE_CON_direction) == 0: #no direction specified for SNE
                direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
                set_direction(SNE_CON, all_rules, direction)                
            
            elif len(SNE_CON_direction) == 1: #single direction specfied for SNE
                direction = next(iter(SNE_CON_direction))
                set_direction(SNE_CON, all_rules, direction)
                   
            elif len(SNE_CON_direction) >1 : #multiple diretions specified for SNE
                raise ValueError ('Opposing directions specified for single number elements')
                
        if len (MNE) >1:#if we have 'multiple number' elements
            
            if len(MNE_direction) == 0: #no direction specified
                direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
                set_direction(MNE, all_rules, direction)
                
            elif len(MNE_direction) ==1: #a single direction specfied
                direction = next(iter(MNE_direction))  
                set_direction(MNE, all_rules, direction)
            elif len (MNE_direction) > 1: 
                for element in MNE_direction:
                    direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
                    set_direction(element, all_rules, direction)           
              
    return (all_rules, seed_list)
    
      

def set_direction (lst, all_rules, direction):
    for element in lst:
        
        for rule in all_rules[element]:
            if isinstance(rule, Rule):
                if rule.rule_type == Ruletype.ARITHMETIC and rule.direction == None:
                    rule.direction = direction
            
    

def assign_layouts(all_rules, SNE_CON, MNE_CON, All_E, seed_list):
    #we will assign a layout to SNE_CON and MNE_CON (only if there are other elements present), we won't assign a layout to MNE_NCON
    layout_elements = SNE_CON + MNE_CON
   
    # define the layouts for addition and subtraction
    
    available_layouts = [
        {(0, 2), (1, 1), (2, 2)},
        {(0, 1), (1, 2), (2, 1)}
    ]

    # list to hold the layouts we will assign
    selected_layouts = []

    # iterate through each element in the arithmetic_non_number_elements list
    if len (All_E)>1:
        
        for element in layout_elements:  
        
            # if there are multiple elements, we should select different layouts for each
            if len(layout_elements) > 1:
            # ensure that layouts differ as much as possible
                selected_layouts_for_element, seed_list = random_choice(seed_list, available_layouts, len(layout_elements))
            else:
                # just pick one layout if only one element
                selected_layouts_for_element, seed_list = random_choice(seed_list, available_layouts, 1)
        
        # loop through each element again to assign its selected layout
            for idx, element in enumerate(layout_elements):
                selected_layout = selected_layouts_for_element[idx]
                selected_layouts.append(selected_layout)  # store the layout for this element

                # set the arithmetic layout for the element
                for rule in all_rules[element]:
                    if isinstance(rule, Rule):
                        if rule.rule_type == Ruletype.ARITHMETIC:
                            rule.arithmetic_layout = selected_layout  # save the selected layout in the rule's arithmetic_layout attribute

    return all_rules, seed_list
