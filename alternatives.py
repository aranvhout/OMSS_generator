import math
from seed import random_shuffle, get_random_attribute
from entity import BigShape, LittleShape, Line, Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linelengths, Linenumbers, Linewidths
import inspect
import copy
from rules import Ruletype

def generate_alternatives(matrices, entity_types, n_alternatives, seed_list, rules):
    # 1. Make a dictionary of each entity and its latest entrances
    alternative_dict = {entity_type: matrices[entity_type][-1][-1] for entity_type in matrices}

   # 2. Generate alternatives for each entity and replace its value in the dictionary
    for key in alternative_dict:
        alternative_dict[key] = generate_alternatives_for_entity(alternative_dict[key], key, n_alternatives, seed_list, rules)

   
    return alternative_dict
    
    
def generate_alternatives_for_entity (entity, entity_type, n_alternatives, seed_list, rules):
    #1 ; list for entity_type
    if entity_type == 'BigShape':
        init_signature = inspect.signature(BigShape.__init__)
        attribute_list = [param for param in init_signature.parameters if param != "self"]
        
    elif entity_type == 'LittleShape':
        init_signature = inspect.signature(LittleShape.__init__)
        attribute_list = [param for param in init_signature.parameters if param != "self"]
        
    elif entity_type == 'Line':
        init_signature = inspect.signature(Line.__init__)
        attribute_list = [param for param in init_signature.parameters if param != "self"]      
    

        
   #2: shuffle attribute list
    attribute_list, seed_list = random_shuffle(seed_list, attribute_list)
    
    #3 save all the non-constant rules in a separate list
    # Get rules for this entity type
    non_constant_attributes = []
    entity_rules = rules.get(entity_type, [])
    for rule in entity_rules:
        if rule.rule_type not in(Ruletype.CONSTANT, Ruletype.FULL_CONSTANT) :
            print(rule.rule_type)
            non_constant_attributes.append(rule.attribute)  # Store attribute_type
            
    #4 reorder the attribute list so that the constant rules get put in last place
    attribute_list[:] = [
    attribute for attribute in attribute_list if attribute.lower() in [str(attr.name).lower() for attr in non_constant_attributes]
    ] + [
    attribute for attribute in attribute_list if attribute.lower() not in [str(attr.name).lower() for attr in non_constant_attributes]
    ]

   
    
    #5: Generate alternatives by change one attribute at time, then using the resulting entities as a new starting point untill number of needed alternatives is reached  
    iterations = math.ceil(math.log(n_alternatives, 2)) #calculate number of iterations
    alternative_list = [entity]
       
    
    
    for i in range(iterations):  
        attribute=attribute_list[i]
        new_alternative_list = []
        for alternative in alternative_list:
            new_alternative_list.extend (modify_attribute(alternative, attribute, seed_list))
            alternative_list = new_alternative_list
    
    selected_alternative_list, seed_list = sample_alternatives(alternative_list, n_alternatives,seed_list)
    return(selected_alternative_list)




def modify_attribute(entity, attribute, seed_list):
    """Modify the given attribute of an entity and return both original and modified versions."""
    # Create an alternative list
    alternative_list = []

    # Store the original entity
    starting_entity = copy.deepcopy(entity)  # Ensure original stays unchanged

    # Get the original value of the attribute
    original_value = getattr(entity, attribute)
    
    #apply constraints
    
    
    # Get a new random value that is different from the original
    new_value, seed_list = get_new_random_value(attribute, seed_list, exclude=original_value)

    # Create a modified entity with the new attribute value
    new_entity = copy.deepcopy(entity)  # Copy original entity
    setattr(new_entity, attribute, new_value)  # Modify the specified attribute

    # Store both original and modified versions
    alternative_list.append(starting_entity)
    alternative_list.append(new_entity)
    
    return alternative_list

def get_new_random_value(attribute, seed_list, exclude=None):
    """Dynamically fetch a random value for the given attribute, ensuring it's not in 'exclude'."""
    enum_class_name = attribute.capitalize() + "s"  # Example: "shape" -> "Shapes"
    
    if enum_class_name not in globals():  
        raise ValueError(f"Unknown attribute: {attribute}")  # Handle invalid attributes

    enum_class = globals()[enum_class_name]  # Retrieve the Enum class dynamically

    # Ensure exclude is a list
    if exclude is None:
        exclude = []
    elif not isinstance(exclude, list):
        exclude = [exclude]

    # Get all possible values, excluding any in the exclude list
    possible_values = [val for val in list(enum_class) if val not in exclude]

    # Ensure there's at least one option left
    if not possible_values:
        raise ValueError(f"No alternative values available for attribute: {attribute}")

    # Get a new random value
    new_value, seed_list = get_random_attribute(seed_list, possible_values)

    return new_value, seed_list



def sample_alternatives(alternative_list, n_alternatives, seed_list):
    assert len(alternative_list) % 2 == 0, "alternative_list must contain an even number of elements"
    assert n_alternatives > len(alternative_list) // 2, "n_alternatives must be more than half of the list size"
    
    half = len(alternative_list) // 2
    first_half = alternative_list[:half]
    second_half = alternative_list[half:]
    
    num_from_each = n_alternatives // 2
    print('alternatives from each half:', num_from_each)
    selected = first_half[:num_from_each] + second_half[:num_from_each]
    
    if n_alternatives % 2 == 1:
        last_pick, seed_list = get_random_attribute(seed_list,  [first_half[num_from_each], second_half[num_from_each]])
        selected.append(last_pick)
    print('selected_alternatives', selected)
    return selected, seed_list
   
        
