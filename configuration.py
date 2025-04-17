from seed import random_choice
from rules import Ruletype, Rule, Configuration
import numpy as np
def configuration_settings(rules, entity_types, seed_list):
    """Ensures all Rule objects have the necessary attributes, setting missing ones to None."""
    
    updated_rules = {}

    for entity, rule_list in rules.items():
        if entity in entity_types:  
            updated_rules[entity] = []
        
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
                updated_rules[entity].append(new_rule)

    #constrain function
    if len(entity_types)>1: #aka multiple entities
        updated_rules, seed_list = constrain (updated_rules, seed_list) #add constraining settings (potentially)
        
    #configuration for alternatives
    updated_rules, seed_list = valid_alternatives(updated_rules, entity_types, seed_list)

    #check whether we need so set an arithmetic layout
    
    has_arithmetic_rule = any(
    any(isinstance(rule, Rule) and rule.rule_type == Ruletype.ARITHMETIC for rule in rule_list)
    for rule_list in updated_rules.values()
)

    if  has_arithmetic_rule is True:
        updated_rules, seed_list = arithmetic_parameters (updated_rules, seed_list)

    # alternatives, in case of multiple entities, we need to update the alternatives 
   # Print the attributes of the object stored in updated_rules['BigShape']
   


    return updated_rules, seed_list


def constrain (updated_rules, seed_list):
    return updated_rules, seed_list



def valid_alternatives(updated_rules, entity_types, seed_list):
    "This determines in which order the entities might be split when it comes to alternatives"
    
    # Step 1: Create an alternative matrix
    matrix = calculate_alternative_matrix(len(entity_types))

    # Step 2: Shuffle the matrix over the rows (to be fixed using an alternative seed)
    np.random.shuffle(matrix)
    print('p', matrix)
    # Step 3: Randomly assign a row for each entity
    for i, entity in enumerate(entity_types):
        # Remove NaNs and convert remaining values to integers
        valid_indices = [int(x) for x in matrix[i] if not np.isnan(x)]
        
        config = Configuration(alternative_indices=valid_indices)
        
        # Ensure Configuration objects are wrapped in a list
        updated_rules[entity].append([config])
    
    return updated_rules, seed_list


    
    
    
    
    

def calculate_alternative_matrix(n_entities):
    columns = 6
    # Initialize the matrix with NaNs
    matrix = np.full((n_entities, columns), np.nan)
    
    # For each column, place a valid integer value in a corresponding row
    for col in range(columns):
        row = col % n_entities  # Ensure we don't go out of bounds
        matrix[row, col] = col + 1  # Place the column index + 1 as the valid value (or any integer)

    return matrix

    
    
    
def arithmetic_parameters(all_rules, seed_list):
    """Handles the arithmetic-related configuration, categorizing entities and assigning layouts."""
    # Step 1: Categorize entities to do some basic checks
    
    SNE_CON, MNE_CON, MNE_NCON, NA_en, All_E = categorize_entities(all_rules)
    
    # Step 2: Select the direction (subtraction, addition) and layout for the entities 
    all_rules, seed_list = select_direction(SNE_CON, MNE_CON, MNE_NCON, all_rules, seed_list)
                    
    # Step 3: Assign layouts to non-number entities (for the number entities this is way less of a haz)
    all_rules, seed_list = assign_layouts(all_rules, SNE_CON, MNE_CON, All_E,  seed_list)
    
    
    return all_rules, seed_list

def categorize_entities(all_rules):
    NA_en = [] #non aritmetic entities
    SNE_CON = [] #single number entities, all rules constant
    SNE_NCON = [] #sinlge number entities, non constant rules
    MNE_CON = [] #multiple numer entities, all rules constant
    MNE_NCON = [] #mulriple number entities, non constant rules
    
    MNE_list = ['line']  # Define multiple number entities
    
    for entity, entity_rules in all_rules.items():
        rule_types = []
        has_arithmetic = False
        is_MNE = entity.lower() in MNE_list
        rules_constant = False
        for rule_obj in entity_rules:
            if isinstance(rule_obj, Rule):
                rule_types.append(rule_obj.rule_type)
                #in case of arithmetic
                if rule_obj.rule_type == Ruletype.ARITHMETIC:
                    has_arithmetic = True            
        if all(rt in {Ruletype.FULL_CONSTANT, Ruletype.CONSTANT, Ruletype.ARITHMETIC} for rt in rule_types):
            rules_constant = True
                   
    
        if has_arithmetic and is_MNE and rules_constant:
            MNE_CON.append (entity)
        
        elif has_arithmetic and is_MNE and not rules_constant:
            MNE_NCON.append (entity)
            
        elif has_arithmetic and not is_MNE and  rules_constant:
            SNE_CON.append (entity)
    
        elif has_arithmetic and not is_MNE and not rules_constant:
            SNE_NCON.append (entity)#at some point we might want to do something with this, for now we raise an error value
            raise ValueError ('All rules should be set to either constant or full constant for an arimethic operation on an entity with only two number options (1 or o)')
            
        else:
            NA_en.append (entity)
            
    All_E =  SNE_CON + MNE_CON + MNE_NCON + NA_en        
    if len(SNE_CON) ==1 and len(All_E) ==1:
        raise ValueError ('Not enough entities to perform an aritmetic operation')
    return (SNE_CON, MNE_CON, MNE_NCON, NA_en, All_E)
    
def select_direction (SNE_CON, MNE_CON, MNE_NCON, all_rules, seed_list):
    #combine valid aritmetic entities in a single list:
    A_E = SNE_CON + MNE_CON  + MNE_NCON
    MNE = MNE_CON + MNE_NCON
    
    #select directions
    # step 1; check whether any direction has been specified
    A_E_direction = set ()
    SNE_CON_direction = set ()
    MNE_direction= set ()
    
    for entity in A_E:    
        
        for rule in all_rules[entity]:
            if isinstance(rule, Rule):
                if rule.rule_type == Ruletype.ARITHMETIC:
                    direction = rule.direction
                    if direction:  # If a direction is specified
                        if direction not in {"addition", "subtraction"}:
                            raise ValueError(f"Invalid direction '{direction}' for entity '{entity}'. Must be 'addition' or 'subtraction'.")
                        elif entity in SNE_CON:
                            SNE_CON_direction.add(direction)
                            A_E_direction.add(direction)
                        elif entity in MNE_CON or entity in MNE_NCON:
                            MNE_direction.add(direction)
                            A_E_direction.add(direction)
                    
    if len(A_E_direction) == 1: #only direction specified, lets use that one for all entities
        direction = next(iter(A_E_direction))
        set_direction(A_E, all_rules, direction)
        
    elif len (A_E_direction) == 0: #not a single direction specified, lets select one for all entities
        direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
        set_direction(A_E, all_rules, direction)
        
    elif len (A_E_direction) > 1 :#multiple directions specified, lets investigate    
        if len(SNE_CON)>0: #if we have single numebr entities
            
            if len(SNE_CON_direction) == 0: #no direction specified for SNE
                direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
                set_direction(SNE_CON, all_rules, direction)                
            
            elif len(SNE_CON_direction) == 1: #single direction specfied for SNE
                direction = next(iter(SNE_CON_direction))
                set_direction(SNE_CON, all_rules, direction)
                   
            elif len(SNE_CON_direction) >1 : #multiple diretions specified for SNE
                raise ValueError ('Opposing directions specified for single number entities')
                
        if len (MNE) >1:#if we have 'multiple number' entities
            
            if len(MNE_direction) == 0: #no direction specified
                direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
                set_direction(MNE, all_rules, direction)
                
            elif len(MNE_direction) ==1: #a single direction specfied
                direction = next(iter(MNE_direction))  
                set_direction(MNE, all_rules, direction)
            elif len (MNE_direction) > 1: #
                for entity in MNE_direction:
                    direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])  
                    set_direction(entity, all_rules, direction)           
              
    return (all_rules, seed_list)
    
      

def set_direction (lst, all_rules, direction):
    for entity in lst:
        
        for rule in all_rules[entity]:
            if isinstance(rule, Rule):
                if rule.rule_type == Ruletype.ARITHMETIC and rule.direction == None:
                    rule.direction = direction
            
    

def assign_layouts(all_rules, SNE_CON, MNE_CON, All_E, seed_list):
    "we will assign a layout to SNE_CON and MNE_CON (only if there are other entities present), we won't assign a layout to MNE_NCON"
    layout_entities = SNE_CON + MNE_CON
   
    # Define the layouts for addition and subtraction
    
    available_layouts = [
        {(0, 2), (1, 1), (2, 2)},
        {(0, 1), (1, 2), (2, 1)}
    ]

    # List to hold the layouts we will assign
    selected_layouts = []

    # Iterate through each entity in the arithmetic_non_number_entities list
    if len (All_E)>1:
        
        for entity in layout_entities:  
        
            # If there are multiple entities, we should select different layouts for each
            if len(layout_entities) > 1:
            # Ensure that layouts differ as much as possible
                selected_layouts_for_entity, seed_list = random_choice(seed_list, available_layouts, len(layout_entities))
            else:
                # Just pick one layout if only one entity
                selected_layouts_for_entity, seed_list = random_choice(seed_list, available_layouts, 1)
        
        # Loop through each entity again to assign its selected layout
            for idx, entity in enumerate(layout_entities):
                selected_layout = selected_layouts_for_entity[idx]
                selected_layouts.append(selected_layout)  # Store the layout for this entity

                # Set the arithmetic layout for the entity
                for rule in all_rules[entity]:
                    if isinstance(rule, Rule):
                        if rule.rule_type == Ruletype.ARITHMETIC:
                            rule.arithmetic_layout = selected_layout  # Save the selected layout in the rule's arithmetic_layout attribute

    return all_rules, seed_list



