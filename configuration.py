from seed import random_choice
from rules import Ruletype, Rule
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

    #check whether we need so set an arithmetic layout
    has_arithmetic_rule = any(
    any(rule.rule_type == Ruletype.ARITHMETIC for rule in rule_list)
    for rule_list in updated_rules.values()
)
    if  has_arithmetic_rule is True:
        updated_rules, seed_list = arithmetic_parameters (updated_rules, seed_list)


    return updated_rules, seed_list


def constrain (updated_rules, seed_list):
    return updated_rules, seed_list




def arithmetic_parameters(all_rules, seed_list):
    """Handles the arithmetic-related configuration, categorizing entities and assigning layouts."""
    # Step 1: Categorize entities to do some basic checks
    arithmetic_number_entities, arithmetic_non_number_entities = categorize_entities(all_rules)
    
    # Step 2: Select the direction (subtraction, addition) and layout for the entities 
    all_rules, seed_list = arithmetic_direction(all_rules, arithmetic_number_entities, arithmetic_non_number_entities, seed_list)
                
    
    # Step 3: Assign layouts to non-number entities (for the number entities this is way less of a haz)
    all_rules, seed_list = assign_layouts(all_rules, arithmetic_non_number_entities,  seed_list)
    
    
    return all_rules, seed_list

def categorize_entities(all_rules):
    """Categorizes entities based on their rules and entity-types (number of not number) into three categories and does some checking."""
    number_entity_list = ['line']  # Define number entities
    non_arithmetic_entities = []
    arithmetic_number_entities = []
    arithmetic_non_number_entities = []

    for entity, entity_rules in all_rules.items():
        #base assumptions for each entity
        has_arithmetic = False
        
        is_number_entity = entity.lower() in number_entity_list
        rule_types = []
        
        for rule_obj in entity_rules:
            rule_types.append(rule_obj.rule_type)
            #in case of arithmetic
            if rule_obj.rule_type == Ruletype.ARITHMETIC:
                has_arithmetic = True
                


       # Categorize based on rule type
        if has_arithmetic:
           if is_number_entity:
               arithmetic_number_entities.append(entity)
              
           else:
               # Validate constant/full constant rules
               if not all(rt in {Ruletype.FULL_CONSTANT, Ruletype.CONSTANT, Ruletype.ARITHMETIC} for rt in rule_types):
                   raise ValueError(f"Entity '{entity}' has an arithmetic rule but contains non-constant rules.")
               
               arithmetic_non_number_entities.append(entity)
               
        else:
           non_arithmetic_entities.append(entity)
    
       
    if  len(arithmetic_non_number_entities) == 1 and len(arithmetic_number_entities) == 0 and len(non_arithmetic_entities) == 0:
          raise ValueError (f"Entity '{entity}' has an arithmetic rule but there a no other entities or to arithmetic over")
    return arithmetic_number_entities, arithmetic_non_number_entities

def arithmetic_direction(all_rules, arithmetic_number_entities, arithmetic_non_number_entities, seed_list):
    """Selects a direction (addition or subtraction) for each arithmetic entity.
       Ensures consistency for non-number entities."""
    
    non_number_directions = set()
    
    # Step 1: Check user-specified directions for non-number entities
    for entity in arithmetic_non_number_entities:
        direction_specified = False
        
        for rule in all_rules[entity]:
            if rule.rule_type == Ruletype.ARITHMETIC:
                direction = rule.direction
                if direction:  # If a direction is specified
                    if direction not in {"addition", "subtraction"}:
                        raise ValueError(f"Invalid direction '{direction}' for entity '{entity}'. Must be 'addition' or 'subtraction'.")
                    non_number_directions.add(direction)
                    direction_specified = True
        
        # Step 2: If no direction was specified for this entity, randomly assign a direction
        if not direction_specified:
            direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])
           
            for rule in all_rules[entity]:
                if rule.rule_type == Ruletype.ARITHMETIC:
                    rule.direction = direction
                    
    # Step 3: Handle conflicting directions for non-number entities
    if len(non_number_directions) > 1:
        raise ValueError(f"Conflicting directions found for non-number entities: {non_number_directions}")
    
    # If there's exactly one direction specified for non-number entities, apply it to all non-number entities
    if len(non_number_directions) == 1:
        selected_direction = non_number_directions.pop()
        
        for entity in arithmetic_non_number_entities:
            for rule in all_rules[entity]:
                if rule.rule_type == Ruletype.ARITHMETIC:
                    rule.direction = selected_direction
                    
    # Step 4: Handle direction for number entities (e.g., 'line')
    for entity in arithmetic_number_entities:
        for rule in all_rules[entity]:
            if rule.rule_type == Ruletype.ARITHMETIC:
                existing_direction = rule.direction
                if existing_direction and existing_direction not in {"addition", "subtraction"}:
                    raise ValueError(f"Invalid direction '{existing_direction}' for entity '{entity}'. Must be 'addition' or 'subtraction'.")
                # If no direction is specified, assign randomly
                if not existing_direction:
                    rule.direction, seed_list = random_choice(seed_list, ["addition", "subtraction"])

    

    return all_rules, seed_list

def assign_layouts(all_rules, arithmetic_non_number_entities, seed_list):
    """Assigns layouts to non-number entities based on their specified direction, with varied layouts for multiple entities."""
    # Define the layouts for addition and subtraction
    addition_layouts = [
        {(0, 0), (1, 1), (2, 0)},
        {(0, 1), (1, 0), (2, 1)}
    ]
    subtraction_layouts = [
        {(0, 2), (1, 1), (2, 2)},
        {(0, 1), (1, 2), (2, 1)}
    ]

    # List to hold the layouts we will assign
    selected_layouts = []

    # Iterate through each entity in the arithmetic_non_number_entities list
    for entity in arithmetic_non_number_entities:
        # Find the direction for this entity from the rules
        direction = None
        for rule in all_rules[entity]:
            if rule.rule_type == Ruletype.ARITHMETIC:
                direction = rule.direction
                break  # We only need the first direction found

        #

        # Now we can just use the direction specified in the rule
        if direction == "addition":
            available_layouts = addition_layouts
        elif direction == "subtraction":
            available_layouts = subtraction_layouts
        
        # If there are multiple entities, we should select different layouts for each
        if len(arithmetic_non_number_entities) > 1:
            # Ensure that layouts differ as much as possible
            selected_layouts_for_entity, seed_list = random_choice(seed_list, available_layouts, len(arithmetic_non_number_entities))
        else:
            # Just pick one layout if only one entity
            selected_layouts_for_entity, seed_list = random_choice(seed_list, available_layouts, 1)
        
        # Loop through each entity again to assign its selected layout
        for idx, entity in enumerate(arithmetic_non_number_entities):
            selected_layout = selected_layouts_for_entity[idx]
            selected_layouts.append(selected_layout)  # Store the layout for this entity

            # Set the arithmetic layout for the entity
            for rule in all_rules[entity]:
                if rule.rule_type == Ruletype.ARITHMETIC:
                    rule.arithmetic_layout = selected_layout  # Save the selected layout in the rule's arithmetic_layout attribute

    return all_rules, seed_list



