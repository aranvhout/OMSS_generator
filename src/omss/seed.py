import random

def seed_generator (seed_value):    
    """creates a seed list based upon a seed value"""
    random.seed(seed_value)
    vector = list(range(99))
    seed_list=random.choices(vector, k=500)#based on the seed,  250 random seeds are drawn from the vector and saved in the seed_list
    random.seed(None)
    return seed_list

def update_seedlist (seed_list):
    """updates the seed list"""
    updated_seed_list=seed_list[1:] + [seed_list[0]] #reshuffle the list, putting the first element in last place      
    return updated_seed_list



def random_choice(seed_list, choices, number=None, exclude=None):
    """randomly selects a choice or multiple choices based upon the seed, allows for excluding options"""
    random.seed(seed_list[0])

    # Ensure exclude is a set for quick lookup
    exclude = set(exclude) if exclude else set()

    # Remove excluded values
    filtered_choices = [c for c in choices if c not in exclude]
  

    if not filtered_choices:  # If all choices are excluded, return empty result
        return None, seed_list

    if number:
        # Get unique choices first
        unique_choices = random.sample(filtered_choices, min(number, len(filtered_choices)))

        # If more choices are needed, repeat from available choices
        remaining_choices = random.choices(unique_choices, k=max(0, number - len(unique_choices)))

        # Combine unique and repeated choices
        attribute = unique_choices + remaining_choices
    else:
        # Select a single random choice
        attribute = random.choice(filtered_choices)

    seed_list = update_seedlist(seed_list)
    random.seed(None)  # Reset randomness

    return attribute, seed_list

def random_rule (seed_list, rules):
   random.seed(seed_list[0])
   rule = random.choice(rules)
   random.seed(None)  # Reset randomness
   return (rule, seed_list)

def random_shuffle (seed_list, input_list):
    """randomly shuffles the input list based upon the seed_list"""
    random.seed(seed_list[0])
    
    random.shuffle(input_list)
    
    seed_list = update_seedlist(seed_list)
    random.seed(None)
    return input_list, seed_list    

