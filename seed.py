import random

def seed_generator (seed_value):    
    random.seed(seed_value)
    vector = list(range(99))
    seed_list=random.choices(vector, k=500)#based on the seed,  250 random seeds are drawn from the vector and saved in the seed_list
    random.seed(None)
    return seed_list

def update_seedlist (seed_list):
    updated_seed_list=seed_list[1:] + [seed_list[0]] #reshuffle the list, putting the first element in last place      
    return updated_seed_list

def random_choice(seed_list, choices, number=None):
    random.seed(seed_list[0])
    
    # Select multiple unique values if number is specified
    if number:        
        attribute = random.sample(choices, min(number, len(choices)))
        
    else:
        # Otherwise, just select a single random value
        attribute = random.choice(choices)
    
    seed_list = update_seedlist(seed_list)
    random.seed(None)
    return attribute, seed_list

def random_shuffle (seed_list, input_list):
    random.seed(seed_list[0])
    
    random.shuffle(input_list)
    
    seed_list = update_seedlist(seed_list)
    random.seed(None)
    return input_list, seed_list    

