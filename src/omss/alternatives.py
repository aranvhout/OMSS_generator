# OMSS imports
from .rules import Ruletype, Rule, AttributeType
from .seed import random_shuffle, random_choice
from .element import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linenumbers,Bigshapenumbers, Littleshapenumbers

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

class Answer:
    def __init__(self, **named_objects):
        # Store each original object by its name (e.g., 'Line', 'BigShape')
        for name, obj in named_objects.items():
            setattr(self, name, obj)

    def split_back(self):
        # Return a dictionary of the original objects
        return {name: getattr(self, name) for name in self.__dict__}

    def __hash__(self):
        # Create a unique hash based on all object attributes
        # Useful if you want to store Answers in a set for uniqueness
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
    
    # combine the matrices in a starting element called answer
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
            new_alternative_list.extend (modify_attribute(alternative, element_type, attribute, seed_list))
            alternative_list = new_alternative_list          
   
    
    if number_elements: #if we have an arithmetic thing going on, the alternatives are created in the same way as before, but then modified a bit  , this doesnt work properly number elements only contains elements with none values
        alternative_list, seed_list = modify_alternatives_with_numbers(alternative_list, number_elements, element_types, seed_list)     
        alternative_list, seed_list = perform_additional_splits(deleted_splits, element_types, alternative_list, iterations, seed_list)    
        alternative_list = improve_alternatives (alternative_list, element_types, deleted_splits, iterations, seed_list)
        
    #sample
    selected_alternative_list, seed_list = sample_alternatives(alternative_list, n_alternatives,seed_list) 
    dis_scores = calculate_dissimilarity_score(selected_alternative_list)
    
    
    return selected_alternative_list, dis_scores
   


def create_attribute_list(answer, element_types, iterations, seed_list, updated_rules):
    non_constant_attributes = []
    constant_attributes = []
    full_constant_attributes = []

    attribute_list = []  # This will store all (element_type, attribute) pairs
    
    # Iterate through each element type
    for element_type in element_types:
              
        # Get the rules for this element type from updated_rules
        element_rules = updated_rules.get(element_type, [])
        
        # Iterate through the rules for this element type
        for rule in element_rules:
            if isinstance(rule, Rule):  # Ensure rule is an instance of Rule
                attribute_type = rule.attribute_type  # Get the attribute type
                
                # Add the element type and attribute to the list (this helps in filtering later)
                attribute_list.append((element_type, attribute_type))
                
                # Categorize attributes based on rule type
                if rule.rule_type == Ruletype.FULL_CONSTANT:
                    full_constant_attributes.append((element_type, attribute_type))  # Save the element_type and attribute_type
                elif rule.rule_type == Ruletype.CONSTANT:
                    constant_attributes.append((element_type, attribute_type))  # Save the element_type and attribute_type
                else:
                    non_constant_attributes.append((element_type, attribute_type))  # Save the element_type and attribute_type
                    
    #some shuffling within each category to prevent preferences
    attribute_list, seed_list = random_shuffle (seed_list, attribute_list)
    
    
    # Reorder the list based on rule categories (non-constant > constant > full-constant)
    ordered_attributes = (
        [(element_type, attr) for element_type, attr in attribute_list if (element_type, attr) in non_constant_attributes] +
        [(element_type, attr) for element_type, attr in attribute_list if (element_type, attr) in constant_attributes] +
        [(element_type, attr) for element_type, attr in attribute_list if (element_type, attr) in full_constant_attributes]
    )
    
    ##modify attribute list, dealing with number attributes
    
    modified_attribute_list, number_elements, deleted_splits = modify_attribute_list (ordered_attributes, iterations, answer, element_types)
    
   
    return modified_attribute_list, number_elements, deleted_splits




def modify_attribute_list(ordered_attributes, n_iterations, answer, element_list):
    """
    1. Removes all attribute tuples for any element in element_list that has None
       for 'number' or 'linenumber' in the answer.
    2. Pushes any ('elementType', AttributeType.NUMBER) tuple from the first n_iterations
       further down the list by swapping it with the next available tuple of the same element.
    3. Finally, ensures that 'NUMBER' attributes are completely removed from the attribute list.
    
    Returns:
    - Modified ordered_attributes list (without 'NUMBER' attributes)
    - List of element types in the order they were removed (first removed first)
    """

    number_fields = ['number', 'linenumber']
    number_elements_ordered = []
    
    deleted_splits = []
    
    # Step 1: Remove elements with missing number-related fields
    for element_type in element_list:
        element = getattr(answer, element_type, None)
        if element:
            for field in number_fields:
                if hasattr(element, field) and getattr(element, field) is None:
                    # Track elements removed due to missing 'number' or 'linenumber'
                    if element_type not in number_elements_ordered:
                        number_elements_ordered.append(element_type)
                        
                        for etype, attr in ordered_attributes:
                            if etype==element_type:
                                if attr.name.lower() not in ['number', 'linenumber']: 
                                    deleted_splits.append((etype, attr))
                        
                        
                        
                    break  # No need to check further fields for this element

    # Remove these elements from ordered_attributes
    ordered_attributes = [
       (etype, attr) for (etype, attr) in ordered_attributes if etype not in number_elements_ordered
    ]
    
   
    # Step 2: Push NUMBER tuples outside of the first n_iterations
    i = 0
    while i < n_iterations:
        if i >= len(ordered_attributes):
            break

        element_type, attribute = ordered_attributes[i]

        if attribute == AttributeType.NUMBER:
            # Track element types with a NUMBER attribute
            if element_type not in number_elements_ordered:
                number_elements_ordered.append(element_type)

            # Look for next attribute with the same element but not NUMBER
            for j in range(i + 1, len(ordered_attributes)):
                next_element, next_attr = ordered_attributes[j]
                if next_element == element_type and next_attr != AttributeType.NUMBER:
                    # Swap positions
                    ordered_attributes[i], ordered_attributes[j] = ordered_attributes[j], ordered_attributes[i]
                    break
            else:
                i += 1
                continue

            continue  # Re-check this position
        i += 1

    # Step 3: Remove all instances of AttributeType.NUMBER from the list
    ordered_attributes = [
        (element_type, attribute) for element_type, attribute in ordered_attributes
        if attribute != AttributeType.NUMBER
    ]

    return ordered_attributes, number_elements_ordered, deleted_splits



def modify_attribute(alternative, element_type, attribute, seed_list):
    """Modify the given attribute of an element and return both original and modified versions."""
    # Create an alternative list
    alternative_list = []
    
    attribute= str(attribute).split('.')[-1].lower()  # Get the name of the enum value, e.g., "NUMBER" from AttributeType.NUMBER, normally I don't like stringmanupulation, 
    #since it can reduce flexibility (eg name that doesnt follow this patern), however in this case both names are totally abritrary so there is no downside

    # Store the original element
    starting_element = copy.deepcopy(alternative)  # Ensure original stays unchanged      
    # Get the correct element from the alternative (Answer)
    element = getattr(alternative, element_type)

    # Get the original value from that element
    original_value = getattr(element, attribute)         
    
    # Get a new random value that is different from the original
    new_value, seed_list = get_new_random_value(attribute, seed_list, exclude=original_value)  

   
    #    Create a modified element with the new attribute value
    new_element_obj = copy.deepcopy(element)
    setattr(new_element_obj, attribute, new_value)
    
    element_dict = alternative.split_back()
    element_dict[element_type] = new_element_obj  # Replace only the modified one
    modified_answer = Answer(**element_dict)
    
    alternative_list.append(starting_element)
    alternative_list.append(modified_answer)
    
    return alternative_list
    

def get_new_random_value(attribute, seed_list, arithmetic = False, exclude=None):
    """ fetch a random value for the given attribute, ensuring it's not in 'exclude'."""
    enum_class = ATTRIBUTE_TO_ENUM.get(attribute)
  
    if arithmetic == True:
        number_enum_classes = [Bigshapenumbers, Linenumbers]
    else:
        number_enum_classes = []
    
    # Ensure exclude is a list
    if exclude is None:
        exclude = []
    elif not isinstance(exclude, list):
        exclude = [exclude]

    
    # Get all possible values, excluding any in the exclude list
    
    possible_values = [val for val in list(enum_class) if val not in exclude]
    if 0 not in exclude and enum_class in number_enum_classes:
        
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
    Modifies up to half of the alternative answers by changing number/linenumber fields
    in the elements listed in element types The process uses `get_safe_candidates` to
    ensure valid modifications and uniqueness.
    """

    # Step 1: Convert None to 0 for removed number/linenumber fields
 
    for ans in alternative_list:
        for element_type in number_elements: 
            element_obj = getattr(ans, element_type, None)
            if element_obj:
                for key in ['number', 'linenumber']:
                    if hasattr(element_obj, key) and getattr(element_obj, key) is None:
                        setattr(element_obj, key, 0)
                        

    number_keys = ['number', 'linenumber']
    modified_elements_per_index = {i: set() for i in range(1, len(alternative_list))}
    modified_indices = set()
    max_modification_list = list(range(len(alternative_list) // 4, len(alternative_list)+1))
    
    max_modifications, seed_list = random_choice(seed_list, max_modification_list)
    all_elements = list(alternative_list[0].__dict__.keys())
    
    
    def filtered_repr(ans):
        repr_dict = {}
        for e_type in all_elements:
            e_obj = getattr(ans, e_type)
            if any(hasattr(e_obj, k) and getattr(e_obj, k) not in [None, 0] for k in number_keys):
                repr_dict[e_type] = {k: v for k, v in e_obj.__dict__.items() if k not in number_keys}
        return repr(repr_dict)

    # Step 2: Process elements one by one
    while len(modified_indices) < max_modifications:
        made_progress = False 
        for element_type in element_types: #i had the idea that this should be arimethic element types, but actually it does work better now, men this code is so complex i will have to recheck it
            
            # 2.1: Get safe candidates for modification
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

            # 3.5 - Check if all number fields across all elements in this answer are now 0 or None
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
               
                continue  # Try again for same or next element

            # Step 4-5: Check uniqueness
            new_repr = filtered_repr(answer_copy)
            all_reprs = {filtered_repr(ans) for i, ans in enumerate(alternative_list) if i != idx_to_modify}
            if new_repr in all_reprs:
               
                continue

            # Step 6: Commit change
            alternative_list[idx_to_modify] = answer_copy
            modified_indices.add(idx_to_modify)
            modified_elements_per_index[idx_to_modify].add(element_type)
          
            made_progress = True

        # If we can't find any valid candidates in the entire loop, we should exit
        if len(modified_indices) >= max_modifications or made_progress == False:
            break

    return alternative_list, seed_list







def get_safe_candidates(element_type, modified_elements_per_index, alternative_list, element_types):
    safe = []
    number_keys = ['number', 'linenumber']
    for i in range(1, len(alternative_list)):
        if element_type in modified_elements_per_index[i]:
            continue
        # Make sure at least one of the *other* elements has a number/linenumber ≠ 0/None
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



def improve_alternatives(alternative_list, element_types, deleted_splits, n_iterations, seed_list):
    answer = alternative_list[0]
    number_keys = ['number', 'linenumber']
    all_elements = list(answer.__dict__.keys())
    
    def filtered_repr(ans):
        repr_dict = {}
        for e_type in all_elements:
            e_obj = getattr(ans, e_type, None)
            if not e_obj:
                continue
            # Only include non-number attributes
            filtered = {
                k: v for k, v in e_obj.__dict__.items()
                if k not in number_keys
            }
            # Skip if element is considered inactive
            if filtered and any(
                hasattr(e_obj, k) and getattr(e_obj, k) not in [None, 0] for k in number_keys
            ):
                repr_dict[e_type] = filtered
        return repr(repr_dict)

    for i in range(1, len(alternative_list)):
        alt = copy.deepcopy(alternative_list[i])
        changed = False

        for e_type in element_types:
            alt_element = getattr(alt, e_type, None)
            answer_element = getattr(answer, e_type, None)

            #  Skip if element is missing or has only None/0 in number keys
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

                if alt_val != ans_val: # print(f"Trying to change {e_type}.{attr} from {alt_val} to {ans_val}")
                   
                    setattr(alt_element, attr, ans_val)

                    # Uniqueness check
                    new_repr = filtered_repr(alt)
                    other_reprs = {
                        filtered_repr(a)
                        for j, a in enumerate(alternative_list)
                        if j != i
                    }

                    if new_repr in other_reprs: #"hange would duplicate an existing alternative. Revertin
                        
                        setattr(alt_element, attr, alt_val)
                    else:
                        
                        changed = True

        if changed:
            alternative_list[i] = alt

    return alternative_list



def perform_additional_splits(deleted_splits, element_types, alternative_list, n_iterations, seed_list):
    "this function is not complete yet, if the number of splits increases however in practice it works for almost 99.99 percent of the cases"
    number_of_splits = n_iterations // len(element_types)
    deleted_split_index = 0
    

    for split_round in range(number_of_splits):
        if deleted_split_index >= len(deleted_splits):
            break  # No more deleted splits to use

        element_type, attribute_type = deleted_splits[deleted_split_index]
        attribute_name = attribute_type.name.lower()

        # Alternate indices: even on 1st split, odd on 2nd, even on 3rd, etc.
        start_index = 1 if split_round % 2 == 0 else 2
        indices_to_modify = [i for i in range(start_index, len(alternative_list), 2)]

        for idx in indices_to_modify:
            # Copy alternative to not modify the original list
            answer_copy = copy.deepcopy(alternative_list[idx])

            # Access the element object to modify
            element_obj = getattr(answer_copy, element_type)
            
            old_value = getattr(element_obj, attribute_name)
           

            # Generate a new random value for the attribute (avoiding the old value)
            new_value, seed_value = get_new_random_value(attribute_name, seed_list, arithmetic = True, exclude=old_value)
            

            # Modify the attribute on the copied element
            setattr(element_obj, attribute_name, new_value)

            # Save the modified copy back to the list
            alternative_list[idx] = answer_copy

            # Log the modification
            

        # Move to next attribute/element pair
        deleted_split_index += 1

    return alternative_list, seed_list



def calculate_dissimilarity_score(selected_alternatives_list):
    compare_to = selected_alternatives_list[0]
    number_keys = {'number', 'linenumber'}
    scores = []

    def normalize(v):
        """Extract enum value if it's an enum, otherwise return as-is."""
        try:
            return v.value
        except AttributeError:
            return v

    def compare_elements(ent1, ent2):
        # Apply the "0 vs non-zero" logic for number keys
        for key in number_keys:
            v1 = normalize(getattr(ent1, key, None))
            v2 = normalize(getattr(ent2, key, None))
            if (v1 == 0 and v2 not in [0, None]) or (v2 == 0 and v1 not in [0, None]):
                return 1  # Early exit: element treated as 1 diff

        # Normal attribute comparison
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
        # Compare all matching fields: BigShape, Line, LittleShape, etc.
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