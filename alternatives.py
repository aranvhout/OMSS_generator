#imports
from rules import Ruletype, Rule
from seed import random_shuffle, random_choice
from entity import BigShape, LittleShape, Line, Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linenumbers,Bigshapenumbers
import inspect
import copy
import math

#dict matching class atributes (eg color of big shape) to classes containing the values (Colors)
ATTRIBUTE_TO_ENUM = {
    'color': Colors,
    'shape': Shapes,
    'size': Sizes,
    'angle': Angles,
    'position': Positions,
    'linetype': Linetypes,
    'number'  : Bigshapenumbers,
    'linenumber': Linenumbers,
}

def generate_alternatives(matrices, entity_types, n_alternatives, seed_list, rules):
    # 1. Make a dictionary of each entity and its latest entrance (in case of multiple entities we will create alternatives for each, then overlay them later)
    alternative_dict = {entity_type: matrices[entity_type][-1][-1] for entity_type in matrices}
    
   # 2. Generate alternatives for each entity and replace its value in the dictionary
    for key in alternative_dict:
        alternative_dict[key] = generate_alternatives_for_entity(alternative_dict[key], key, n_alternatives, seed_list, rules)
        #note to self dict[key], refers to the value associated with that key, in this case the entity(value) for a specific entity type
   
    return alternative_dict
    
    
def generate_alternatives_for_entity (entity, entity_type, n_alternatives, seed_list, rules):
    #1 ; list attributes for the specified entity_type
    if entity_type == 'BigShape':
        init_signature = inspect.signature(BigShape.__init__)
        attribute_list = [param for param in init_signature.parameters if param != "self"]
        
    elif entity_type == 'LittleShape':
        init_signature = inspect.signature(LittleShape.__init__)
        attribute_list = [param for param in init_signature.parameters if param != "self"]
        
    elif entity_type == 'Line':
        init_signature = inspect.signature(Line.__init__)
        attribute_list = [param for param in init_signature.parameters if param != "self"]      
            


          
        
    # 2: Reorder the attribute list based upon the rules, we will manipulate the splitting order to the make the alternatives more believable
    full_constant_attributes = []
    constant_attributes = []
    non_constant_attributes = []

    # Categorize attributes based on rule type
    entity_rules = rules.get(entity_type, [])

    for rule in entity_rules: #WHAT about attributes for which a rule is not specified
        if isinstance(rule, Rule):  # Ensure rule is an instance of Rule
            if rule.rule_type == Ruletype.FULL_CONSTANT:
                full_constant_attributes.append(rule.attribute_type)
            elif rule.rule_type == Ruletype.CONSTANT:
                constant_attributes.append(rule.attribute_type)
            else:
                non_constant_attributes.append(rule.attribute_type)

    
    # Convert to lowercase, the entity classes have lowercase whereas the enum classes are uppercase,
    non_constant_names = [attr.name.lower() for attr in non_constant_attributes]
    constant_names = [attr.name.lower() for attr in constant_attributes]
    full_constant_names = [attr.name.lower() for attr in full_constant_attributes]
   
       
    attribute_list, seed_list = random_shuffle(seed_list, attribute_list)

    # Sort attributes: (1) non-constant first, (2) constant next, (3) full-constant last
    attribute_list[:] = (
        [attr for attr in attribute_list if attr.lower() in non_constant_names] +
        [attr for attr in attribute_list if attr.lower() in constant_names] +
        [attr for attr in attribute_list if attr.lower() in full_constant_names]
        )

    
    #complicated code to get the indices out for the potential skip values (maybe one day i have time to conscise my code)
    for item in rules[entity_type]:
        if isinstance(item, list):  # Check if the item is a list
            for sub_item in item:
                if hasattr(sub_item, 'alternative_indices'):
                    indices = sub_item.alternative_indices
                    
    
    #5: Generate alternatives by change one attribute at time, then using the resulting entities as a new starting point untill number of needed alternatives is reached  
    iterations = math.ceil(math.log(n_alternatives, 2)) #calculate number of iterations
    attribute_list,  contains_number=modify_attribute_list(indices, iterations, attribute_list)
    


    
    alternative_list = [entity]      
       
    for i in range(iterations):  
        attribute=attribute_list[i]
        new_alternative_list = []
        for alternative in alternative_list:            
            new_alternative_list.extend (modify_attribute(alternative, attribute, seed_list))
            alternative_list = new_alternative_list
            
    print(attribute_list)         
    if contains_number: #in case of a number variable we perform an additional split!  
       
        #alternative_list, seed_list = number_modify(alternative_list, seed_list)
        pass
    selected_alternative_list, seed_list = sample_alternatives(alternative_list, n_alternatives,seed_list)
    return(selected_alternative_list)


#REMOVE INDEX FROM SPLITTING ORDER
def add_number (attribute_list, iteration):
    #replace the final split by number
    if attribute_list[iteration] != 'skip':
        attribute_list[iteration] = 'number'
        
    return attribute_list





def number_modify(alternative_list, seed_list):
    if len(alternative_list) % 4 != 0:
        raise ValueError("The length of the list must be divisible by 4.")

    # We'll print the IDs and the original values of entities before modifying
  

    for i in range(0, len(alternative_list), 4):
        # Loop through the middle two entities in each chunk of 4
        for j in [i + 1, i + 2]:
            # Get the original entity at index j
            entity = alternative_list[j]

            # Print the entity's original value and id
            original_value = getattr(entity, 'number')
           

            # Make a deep copy of the entity to ensure no references are shared
            entity_copy = copy.deepcopy(entity)

            # Get a new random value that excludes the original value
            new_value, seed_list = get_new_random_value('number', seed_list, exclude=original_value)

            # Print the new value
            

            # Modify the copied entity
            setattr(entity_copy, 'number', new_value)

            # Place the new modified entity back in the original list
            alternative_list[j] = entity_copy

           

    return alternative_list, seed_list







    
    
    
def modify_attribute_list(indices, iterations, attribute_list):
    'inserts skip values to make sure we do not split by multiple attribute for a single grid'
    result = []
    attr_index = 0
    contains_number = False         
    
    for i in range(1, 7):  # Always output exactly 6 elements (plenty of alternatives with 2^6) #some entities have only three attributes orso, we cant reiterate them, so give error message?
        if i in indices and attr_index < len(attribute_list):
            result.append(attribute_list[attr_index])
            attr_index += 1
        else:
            result.append("skip")
            
    if 'number' in result[0:iterations]:
        contains_number = True
        alternative_to_number = None
        for attr in attribute_list:#not sure what we should do if runs out of valid attributes.
            if attr not in result[0:iterations]:
                alternative_to_number = attr
                break

        result = [alternative_to_number if x == 'number' else x for x in result]

        print('tos', attribute_list)
    return result,  contains_number  
    
    
    pass
def modify_attribute(entity, attribute, seed_list):
    """Modify the given attribute of an entity and return both original and modified versions."""
    # Create an alternative list
    alternative_list = []

    # Store the original entity
    starting_entity = copy.deepcopy(entity)  # Ensure original stays unchanged      
    
    if attribute not in ['skip', 'number']:    #we modify the starting entity
        # Get the original value of the attribute
        original_value = getattr(entity, attribute)                 
    # Get a new random value that is different from the original
        new_value, seed_list = get_new_random_value(attribute, seed_list, exclude=original_value)        
    #    Create a modified entity with the new attribute value
        new_entity = copy.deepcopy(entity)  # Copy original entity
        setattr(new_entity, attribute, new_value)  # Modify the specified attribute
      
        alternative_list.append(starting_entity)
        alternative_list.append(new_entity)
      
    elif attribute == 'skip': #we simply copy the starting entitity
        new_entity = copy.deepcopy(entity)
        alternative_list.append(starting_entity)
        alternative_list.append(new_entity)
        
    elif attribute == 'number': #basically we do nothing
        
        alternative_list.append(starting_entity)
        
   
    
    
    return alternative_list

def get_new_random_value(attribute, seed_list, exclude=None):
    """ fetch a random value for the given attribute, ensuring it's not in 'exclude'."""
    enum_class = ATTRIBUTE_TO_ENUM.get(attribute)
    
    # Ensure exclude is a list
    if exclude is None:
        exclude = []
    elif not isinstance(exclude, list):
        exclude = [exclude]

    
    # Get all possible values, excluding any in the exclude list
    possible_values = [val for val in list(enum_class) if val not in exclude]
    if enum_class == Bigshapenumbers:
        possible_values.append (0)
    # Ensure there's at least one option left (eg lets say we have an attribute with only one option)
    if not possible_values:
        raise ValueError(f"No alternative values available for attribute: {attribute}")

    # Get a new random value
    new_value, seed_list = random_choice(seed_list, possible_values)

    return new_value, seed_list


def sample_alternatives(alternative_list, n_alternatives, seed_list):
    "samples a subset of alternatives if needed"
    assert len(alternative_list) % 2 == 0, "alternative_list must contain an even number of elements (always the case in theory)"
    assert n_alternatives > len(alternative_list) // 2, "n_alternatives must be more than half of the list size (always the case in theory)"
   
    #split the original alternative list in two halves (I can explain why i did it like this, in short it creates a better set of alternatives since you consider the first split)
    half = len(alternative_list) // 2
    first_half = alternative_list[:half]
    second_half = alternative_list[half:]
    
    #get the first x alternatives from both halve
    num_from_each = n_alternatives // 2
   
    selected = first_half[:num_from_each] + second_half[:num_from_each]
    
    #in case of uneven number of alternatives, select an additional random alternative from a half
    if n_alternatives % 2 == 1:
        last_pick, seed_list = random_choice(seed_list,  [first_half[num_from_each], second_half[num_from_each]])
        selected.append(last_pick)
    
    return selected, seed_list
   
        
def get_safe_candidates(entity_type, modified_entities_per_index, alternative_list, number_entities):
    safe = []
    number_keys = ['number', 'linenumber']
    for i in range(1, len(alternative_list)):
        if entity_type in modified_entities_per_index[i]:
            continue
        # Make sure at least one of the *other* entities has a number/linenumber ≠ 0/None
        has_nonzero_other = False
        for other_entity in number_entities:
            if other_entity == entity_type:
                continue
            other_obj = getattr(alternative_list[i], other_entity, None)
            if other_obj and any(
                hasattr(other_obj, key) and getattr(other_obj, key) not in [None, 0]
                for key in number_keys
            ):
                has_nonzero_other = True
                break
        if has_nonzero_other:
            safe.append(i)
    return safe
