#imports
from rules import Ruletype
from seed import random_shuffle, random_choice
from entity import BigShape, LittleShape, Line, Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linenumbers
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
            
   #2: shuffle attribute list
    attribute_list, seed_list = random_shuffle(seed_list, attribute_list)
     
    # 3: Reorder the attribute list based upon the rules, we will manipulate the splitting order to the make the alternatives more believable
    full_constant_attributes = []
    constant_attributes = []
    non_constant_attributes = []

    # Categorize attributes based on rule type
    entity_rules = rules.get(entity_type, [])
    for rule in entity_rules:
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

    # Sort attributes: (1) non-constant first, (2) constant next, (3) full-constant last
    attribute_list[:] = (
        [attr for attr in attribute_list if attr.lower() in non_constant_names] +
        [attr for attr in attribute_list if attr.lower() in constant_names] +
        [attr for attr in attribute_list if attr.lower() in full_constant_names]
        )

      
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
#REMOVE INDEX FROM SPLITTING ORDER

def modify_attribute(entity, attribute, seed_list):
    """Modify the given attribute of an entity and return both original and modified versions."""
    # Create an alternative list
    alternative_list = []

    # Store the original entity
    starting_entity = copy.deepcopy(entity)  # Ensure original stays unchanged

    # Get the original value of the attribute
    original_value = getattr(entity, attribute)
      
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
    """ fetch a random value for the given attribute, ensuring it's not in 'exclude'."""
    enum_class = ATTRIBUTE_TO_ENUM.get(attribute)
   
    # Ensure exclude is a list
    if exclude is None:
        exclude = []
    elif not isinstance(exclude, list):
        exclude = [exclude]

    # Get all possible values, excluding any in the exclude list
    possible_values = [val for val in list(enum_class) if val not in exclude]

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
   
        
