# OMSS imports
from .rules import Ruletype, Rule, AttributeType
from .seed import random_shuffle, random_choice, update_seedlist
from .element import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linenumbers,Bigshapenumbers, Littleshapenumbers, LittleShape

#general imports
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
    'littleshapenumber'  : Littleshapenumbers,
    
}

class Answer: #answer class that combines the different elementypes into one
    def __init__(self, **named_objects):
        # store each original object by its name 
        for name, obj in named_objects.items():
            setattr(self, name, obj)

    def split_back(self):
        # return a dictionary of the original objects
        return {name: getattr(self, name) for name in self.__dict__}

    def __hash__(self):
       
        return hash(tuple(
            (name, tuple(sorted(vars(getattr(self, name)).items())))
            for name in sorted(self.__dict__)
        ))

    def __eq__(self, other):
        if not isinstance(other, Answer):
            return False
        return all(
            vars(getattr(self, name)) == vars(getattr(other, name))
            for name in self.__dict__
        )

    def __repr__(self):
        parts = []
        for name, obj in self.__dict__.items():
            obj_attrs = vars(obj)
            parts.append(f"{name}={obj_attrs}")
        return f"Answer({', '.join(parts)})"




def create_alternatives(matrices, element_types, n_alternatives, seed_list, updated_rules):
    
    # combine the last index of the matrix (or matrices) in a starting element called answer
    alternative_dict = {element_type: matrices[element_type][-1][-1] for element_type in matrices}
    answer = Answer(**alternative_dict)
   
    #calculate how many iterations (splits in the tree) we need
    iterations = math.ceil(math.log(n_alternatives, 2)) #calculate number of iterations
        
    #create attribute list,1) with a preference for non-constant attributes 
    attribute_list, number_elements, deleted_splits = create_attribute_list (answer, element_types, iterations, seed_list, updated_rules)
   
    #alternatives
    alternative_list = [answer]
    if iterations > len(attribute_list):
        raise ValueError("Too many alternatives for the specific setting. Please lower the number of alternatives.")

    for i in range(iterations):  
        element_type, attribute=attribute_list[i]
        new_alternative_list = []
        
        for alternative in alternative_list:             
            #this is superugly and I regret ever improving littleshape, we need to set a seed for littleshape to account for the random position
            LittleShape.reset_seed()
            LittleShape.set_seed(seed_list[0])
            seed_list = update_seedlist(seed_list) 
            
            #create the new alternatives
            new_alternative_list.extend (modify_attribute(alternative, element_type, attribute, seed_list))
            alternative_list = new_alternative_list          
   
   
    if number_elements: #if we have an arithmetic thing going on (WITH A LAYOUT, aka meaning 0/None values are present), the alternatives are created in the same way as before, but then modified a bit  ,
        alternative_list, seed_list = modify_alternatives_with_numbers(alternative_list, number_elements, element_types, seed_list)     
        alternative_list, seed_list = perform_additional_splits(deleted_splits, element_types, alternative_list, iterations, seed_list)       
        alternative_list = improve_alternatives (alternative_list, element_types, deleted_splits, iterations, seed_list)
        
    #sample
    selected_alternative_list, seed_list = sample_alternatives(alternative_list, n_alternatives,seed_list) 
    
    #dissimilarity scores
    dis_scores = calculate_dissimilarity_score(selected_alternative_list)
    
    return selected_alternative_list, dis_scores
   


def create_attribute_list(answer, element_types, iterations, seed_list, updated_rules):
    "creates a list of attributes to modify based upon the specified rules"
    non_constant_attributes = []
    constant_attributes = []
    full_constant_attributes = []

    attribute_list = []  # this will store all (element_type, attribute) pairs
    
    # iterate through each element type and find cool attributes to modify
    for element_type in element_types:              
    
        element_rules = updated_rules.get(element_type, [])
        
        for rule in element_rules:
            if isinstance(rule, Rule): 
                attribute_type = rule.attribute_type  # get the attribute type      
                attribute_list.append((element_type, attribute_type))
                
                # categorize attributes based on rule type
                if rule.rule_type == Ruletype.FULL_CONSTANT:
                    full_constant_attributes.append((element_type, attribute_type))  
                elif rule.rule_type == Ruletype.CONSTANT:
                    constant_attributes.append((element_type, attribute_type)) 
                else:
                    non_constant_attributes.append((element_type, attribute_type))  
                    
    #some shuffling within each category to prevent preferences (eg could be that the order in which
    #the rules are specified in the rules dictionairy affects this)
    attribute_list, seed_list = random_shuffle (seed_list, attribute_list)
        
    # reorder the list based on rule categories (non-constant > constant > full-constant)
    ordered_attributes = (
        [(element_type, attr) for element_type, attr in attribute_list if (element_type, attr) in non_constant_attributes] +
        [(element_type, attr) for element_type, attr in attribute_list if (element_type, attr) in constant_attributes] +
        [(element_type, attr) for element_type, attr in attribute_list if (element_type, attr) in full_constant_attributes]
    )
    
    #modify attribute list, dealing with number attributes by essentially removing them. Number attributes are dealt with later    
    modified_attribute_list, number_elements, deleted_splits = modify_attribute_list (ordered_attributes, iterations, answer, element_types)
    
   
    return modified_attribute_list, number_elements, deleted_splits




def modify_attribute_list(ordered_attributes, n_iterations, answer, element_list):
    """this is only relevant for arithmetic rules with a arithmetic layout and only specifically when there is none valeu for the answer! (need to fix this someday, it needs to be looking at the layout instead of the final cell in the matric)
  deals with binomianal number (AKA BIGSHAPE NUMBERS) attributes by 1) tracking and 2) removing them. The number attributes that would have been changed then get modified later. It also removes any element with 
a None value for a number field (which only happens in case of a layout) since modifying attributes of these element wont do anything (none means the element wont be rendered). So this is really only relevant for arithmetic in combination with a layout"""

    number_fields = ['number','littleshapenumber', 'linenumber']
    number_elements_ordered = []
    
    deleted_splits = []
    
    # step 1: entirely remove elements with "None" number-related fields (we will deal with them even later)
    for element_type in element_list:
        element = getattr(answer, element_type, None)
        if element:
            for field in number_fields:
               
                if hasattr(element, field) and getattr(element, field) is None:
                    
                    # track elements removed due to missing 'number' or 'linenumber' or littleshapenumber
                    if element_type not in number_elements_ordered:
                        number_elements_ordered.append(element_type)
                        
                        for etype, attr in ordered_attributes:
                            if etype==element_type:
                                if attr.name.lower() not in ['number', 'linenumber', 'littleshapenumber']: 
                                    deleted_splits.append((etype, attr))
                        
                        
                        
                    break  # no need to check further fields for this element

    # remove these elements from ordered_attributes
    ordered_attributes = [
       (etype, attr) for (etype, attr) in ordered_attributes if etype not in number_elements_ordered
    ]
    
   
    # step 2: push NUMBER tuples outside of the first n_iterations and replace it by the next non number tupple (we deal with them later),
    #importantly track the number tupples we pushed out!
    i = 0
    while i < n_iterations:
        if i >= len(ordered_attributes):
            break

        element_type, attribute = ordered_attributes[i]

        if attribute == AttributeType.NUMBER:
            # track element types with a NUMBER attribute
            if element_type not in number_elements_ordered:
                number_elements_ordered.append(element_type)

            # look for next attribute with the same element but not NUMBER
            for j in range(i + 1, len(ordered_attributes)):
                next_element, next_attr = ordered_attributes[j]
                if next_element == element_type and next_attr != AttributeType.NUMBER:
                    # swap positions
                    ordered_attributes[i], ordered_attributes[j] = ordered_attributes[j], ordered_attributes[i]
                    break
            else:
                i += 1
                continue

            continue  # Re-check this position
        i += 1

    # step 3: finally remove all instances of AttributeType.NUMBER from the list (diff between step 2 and 3 is, that we now also track the order of number attributes we removed)
    ordered_attributes = [
        (element_type, attribute) for element_type, attribute in ordered_attributes
        if attribute != AttributeType.NUMBER
    ]

    return ordered_attributes, number_elements_ordered, deleted_splits



def modify_attribute(alternative, element_type, attribute, seed_list):
    """modify the given attribute of an element and return both original and modified versions.
    this is the workhorse of creating the alternatives"""
    #create an alternative list
    alternative_list = []
    
    attribute= str(attribute).split('.')[-1].lower()  # get the name of the enum value, e.g., "NUMBER" from AttributeType.NUMBER, normally I don't like stringmanupulation, 
    #since it can reduce flexibility (eg name that doesnt follow this patern), however in this case both names are totally abritrary so there is no downside

    # store the original element
    starting_element = copy.deepcopy(alternative)    
    # get the correct element from the alternative (aka theAnswer)
    element = getattr(alternative, element_type)

    # get the original value from that element
    original_value = getattr(element, attribute)         
    
    # get a new random value that is different from the original
    new_value, seed_list = get_new_random_value(attribute, seed_list, exclude=original_value)  
   
    #create a modified element with the new attribute value
    new_element_obj = copy.deepcopy(element)
    setattr(new_element_obj, attribute, new_value)
    
    element_dict = alternative.split_back()
    element_dict[element_type] = new_element_obj  # replace only the modified one
    modified_answer = Answer(**element_dict)
    
    alternative_list.append(starting_element)
    alternative_list.append(modified_answer)
    
    return alternative_list
    

def get_new_random_value(attribute, seed_list, arithmetic = False, exclude=None):
    """ get a random value for the given attribute, ensuring it's not in 'exclude'."""
    enum_class = ATTRIBUTE_TO_ENUM.get(attribute)
  
    if arithmetic == True:
        number_enum_classes = [Bigshapenumbers, Littleshapenumbers, Linenumbers]
    else:
        number_enum_classes = []
    
    # ensure exclude is a list
    if exclude is None:
        exclude = []
    elif not isinstance(exclude, list):
        exclude = [exclude]

    
    # get all possible values excluding any in the exclude list    
    possible_values = [val for val in list(enum_class) if val not in exclude]
    if 0 not in exclude and enum_class in number_enum_classes: #append zero as a potential value for number splits        
        possible_values.append (0)
    # ensure there's at least one option left (eg lets say we have an attribute with only one option)
    if not possible_values:
        raise ValueError(f"No alternative values available for attribute: {attribute}")

    # gt a new random value
    new_value, seed_list = random_choice(seed_list, possible_values)

    return new_value, seed_list   


def sample_alternatives(alternative_list, n_alternatives, seed_list):
    "samples a subset of alternatives if needed"
    assert len(alternative_list) % 2 == 0, "alternative_list must contain an even number of elements (always the case in theory)"
    assert n_alternatives > len(alternative_list) // 2, "n_alternatives must be more than half of the list size (always the case in theory)"
   
    #split the original alternative list in two halves (I can explain why i did it like this, in short it creates a better set of alternatives since you weigh the first split more)
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
   


def modify_alternatives_with_numbers(alternative_list, number_elements, element_types, seed_list):
    """
    modifies up to half of the alternative answers by changing number/linenumber fields
    in the elements listed in element types 
    """

    # step 1: convert None to 0 for removed number/linenumber fields 
    for ans in alternative_list:
        for element_type in number_elements: 
            element_obj = getattr(ans, element_type, None)
            if element_obj:
                for key in ['number', 'linenumber', 'littleshapenumber']:
                    if hasattr(element_obj, key) and getattr(element_obj, key) is None:
                        setattr(element_obj, key, 0)
                        

    # 1.5: how many alternatives we want to modify, we don't want to change too many
    number_keys = ['number', 'linenumber', 'littleshapenumber']
    modified_elements_per_index = {i: set() for i in range(1, len(alternative_list))}
    modified_indices = set()
    max_modification_list = list(range(len(alternative_list) // 4, len(alternative_list)+1))    
    max_modifications, seed_list = random_choice(seed_list, max_modification_list)
    
    all_elements = list(alternative_list[0].__dict__.keys())
    
      
    #in the next steps we we will select an alternative and change its number value, we will perform check to ensure that this change won't result in an empty grid
    #moreover, the change shouldnt result in multiple copies of an alternative. only if these checks are passed, we commmit the change
    # step 2: process elements one by one
    while len(modified_indices) < max_modifications:
        made_progress = False 
        for element_type in element_types: #i had the idea that this should be arimethic element types, but actually it does work better now, men this code is so complex i will have to recheck it
            
            # 2.5: get safe candidates for modification (meaning that a change in the number value won't result in an empty grid)
            candidates = get_safe_candidates(element_type, modified_elements_per_index, alternative_list, element_types)
            
            if not candidates:
               
                continue
            
            idx_to_modify, seed_list = random_choice(seed_list, candidates)
           
            answer_copy = copy.deepcopy(alternative_list[idx_to_modify])
            element_obj = getattr(answer_copy, element_type)
            key_to_modify = next((k for k in number_keys if hasattr(element_obj, k)), None)
            if not key_to_modify:
                continue

            current_value = getattr(element_obj, key_to_modify)
            new_value, seed_list = get_new_random_value(key_to_modify, seed_list, arithmetic = True, exclude=current_value)
            
            setattr(element_obj, key_to_modify, new_value)
            
            # 3.5 check if all number fields across all elements in this answer are now 0 or None, basically a safeguard since step 2.5 should already prevent this
            all_zero = True
            for e_type in all_elements:
                e_obj = getattr(answer_copy, e_type)
                for k in number_keys:
                    if hasattr(e_obj, k) and getattr(e_obj, k) not in [None, 0]:
                        all_zero = False
                        break
                if not all_zero:
                    break

            if all_zero:
               
                continue  # try again for same or next element

            # step 4-5: check uniqueness (we dont want multiple copies of an alternative)
            def filtered_repr(ans):
                repr_dict = {}
                for e_type in all_elements:
                    e_obj = getattr(ans, e_type)
                    if any(hasattr(e_obj, k) and getattr(e_obj, k) not in [None, 0] for k in number_keys):
                        repr_dict[e_type] = {k: v for k, v in e_obj.__dict__.items() if k not in number_keys}
                        
                return repr(repr_dict)
            
            new_repr = filtered_repr(answer_copy)
            all_reprs = {filtered_repr(ans) for i, ans in enumerate(alternative_list) if i != idx_to_modify}
            if new_repr in all_reprs:
               
                continue

            # step 6: all checks are passed and we commit the change
            alternative_list[idx_to_modify] = answer_copy
            modified_indices.add(idx_to_modify)
            modified_elements_per_index[idx_to_modify].add(element_type)
          
            made_progress = True

        # if we can't find any valid candidates in the entire loop, we should exit
        if len(modified_indices) >= max_modifications or made_progress == False:
            break

    return alternative_list, seed_list




def get_safe_candidates(element_type, modified_elements_per_index, alternative_list, element_types):
    #checks whether we can change the number attribute of an element without accidently creating an empty grid
    safe = []
    number_keys = ['number', 'linenumber', 'littleshapenumber']
    for i in range(1, len(alternative_list)):
        if element_type in modified_elements_per_index[i]:
            continue
        # make sure at least one of the other elements has a number/linenumber ≠ 0/None
        has_nonzero_other = False
        for other_element in element_types:
            if other_element == element_type:
                continue
            other_obj = getattr(alternative_list[i], other_element, None)
            if other_obj and any(
                hasattr(other_obj, key) and getattr(other_obj, key) not in [None, 0]
                for key in number_keys
            ):
                has_nonzero_other = True
                break
        if has_nonzero_other:
            safe.append(i)
      
    return safe

def perform_additional_splits(deleted_splits, element_types, alternative_list, n_iterations, seed_list):
    "additional splits for the elements with a none value to make better alternatives" 
    #most of the times the working part of this function is not exceuted since there are no more splits available
    #in addition, even when its executed the changes might be reverted by the improve_alternatives function. in conclusion
    #this code is a bit redudant tbf
    number_of_splits = n_iterations // len(element_types)
    deleted_split_index = 0
    

    for split_round in range(number_of_splits):
        if deleted_split_index >= len(deleted_splits):
            
            break  # no more deleted splits to use

        element_type, attribute_type = deleted_splits[deleted_split_index]
        attribute_name = attribute_type.name.lower()

        # alternate indices: even on 1st split, odd on 2nd, even on 3rd, etc.
        start_index = 1 if split_round % 2 == 0 else 2
        indices_to_modify = [i for i in range(start_index, len(alternative_list), 2)]

        for idx in indices_to_modify:
            
            answer_copy = copy.deepcopy(alternative_list[idx])

           
            element_obj = getattr(answer_copy, element_type)
            
            old_value = getattr(element_obj, attribute_name)
           

            # generate a new random value for the attribute (avoiding the old value)
            new_value, seed_value = get_new_random_value(attribute_name, seed_list, arithmetic = True, exclude=old_value)
            

            # modify the attribute on the copied element
            setattr(element_obj, attribute_name, new_value)

            # save the modified copy back to the list
            alternative_list[idx] = answer_copy

         

        # move to next attribute/element pair
        deleted_split_index += 1

    return alternative_list, seed_list


def improve_alternatives(alternative_list, element_types, deleted_splits, n_iterations, seed_list):
    """almost done; basically by messing with the number attribute, we essentially performed a 0.5 additional alternative split, now we 
    compensate a bit for that by trying to modify the alternatives to look more like the correct answer while preventing a copy. Obv we dont touch the number attributes anymore
    or else we might revert our earlier changes"""
    answer = alternative_list[0]
    number_keys = ['number', 'linenumber', 'littleshapenumber']
    all_elements = list(answer.__dict__.keys())
    
    def filtered_repr(ans):
        repr_dict = {}
        for e_type in all_elements:
           
            e_obj = getattr(ans, e_type, None)
            if not e_obj:
                continue
            # only include non-number attributes
            filtered = {
                k: v for k, v in e_obj.__dict__.items()
                if k not in number_keys
            }
            # skip if element is basically empty (eg none values; changign this element wont result in visual changes)
            if filtered and any(
                hasattr(e_obj, k) and getattr(e_obj, k) not in [None, 0] for k in number_keys
            ):
                repr_dict[e_type] = filtered
        return repr(repr_dict)

    for i in range(1, len(alternative_list)):
        alt = copy.deepcopy(alternative_list[i])
        changed = False

        for e_type in element_types:
            if e_type == "LittleShape": #for extremely complex reasons we just gotta avoid this section for littleshape, it has to do with the coupling of position and number
                continue  # 
            alt_element = getattr(alt, e_type, None)
            answer_element = getattr(answer, e_type, None)

            #  skip if element is missing or has only None/0 in number keys
            if not alt_element or all(
                not hasattr(alt_element, k) or getattr(alt_element, k) in [None, 0]
                for k in number_keys
            ):
                continue

            for attr in alt_element.__dict__:
                if attr in number_keys:
                    continue

                alt_val = getattr(alt_element, attr)
                ans_val = getattr(answer_element, attr)

                if alt_val != ans_val: #
                   
                    
                    setattr(alt_element, attr, ans_val)

                    #  check uniqueness
                    new_repr = filtered_repr(alt)
                    other_reprs = {
                        filtered_repr(a)
                        for j, a in enumerate(alternative_list)
                        if j != i
                    }

                    if new_repr in other_reprs: 
                        
                        setattr(alt_element, attr, alt_val)
                    else:
                        
                        changed = True

        if changed:
            alternative_list[i] = alt

    return alternative_list



def calculate_dissimilarity_score(selected_alternatives_list):
    """this is simply code for calculating how different each alternative is, we need it for the output file"""
    compare_to = selected_alternatives_list[0]
    number_keys = {'number', 'linenumber', 'littleshapenumber'}
    scores = []

    def normalize(v):        
        try:
            return v.value
        except AttributeError:
            return v

    def compare_elements(ent1, ent2):
        # zero element is calculated as being one point different from a present element
        for key in number_keys:
            v1 = normalize(getattr(ent1, key, None))
            v2 = normalize(getattr(ent2, key, None))
            if (v1 == 0 and v2 not in [0, None]) or (v2 == 0 and v1 not in [0, None]):
                return 1  # early exit: element treated as 1 diff

        # normal attribute comparison
        diff = 0
        all_attrs = set(vars(ent1).keys()).union(vars(ent2).keys())
        for attr in all_attrs:
            v1 = normalize(getattr(ent1, attr, None))
            v2 = normalize(getattr(ent2, attr, None))
            if v1 is None and v2 is None:
                continue
            if v1 != v2:
                diff += 1
        return diff

    for alt in selected_alternatives_list:
        total_diff = 0
        # compare all matching fields (bigshape to bigshape etc)
        subelements = set(vars(compare_to).keys()).union(vars(alt).keys())
        for key in subelements:
            ent1 = getattr(compare_to, key, None)
            ent2 = getattr(alt, key, None)
            if ent1 is None and ent2 is None:
                continue
            elif ent1 is None or ent2 is None:
                total_diff += 1
            else:
                total_diff += compare_elements(ent1, ent2)
        scores.append(total_diff)

    return scores