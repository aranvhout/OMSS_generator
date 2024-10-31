import random

def seed_generator (seed_value):    
    random.seed(seed_value)
    vector = [0,1,2,3,4,5,6,7,8,9]
    seed_list=random.choices(vector, k=500)#based on the seed,  250 random seeds are drawn from the vector and saved in the seed_list
    random.seed(None)
    return seed_list

def update_seedlist (seed_list):
    updated_seed_list=seed_list[1:] + [seed_list[0]] #reshuffle the list, putting the first element in last place      
    return updated_seed_list

def get_random_attribute(seed_list, choices):
    random.seed(seed_list[0])
    attribute = random.choice(choices)
    seed_list=update_seedlist(seed_list)
    return attribute, seed_list