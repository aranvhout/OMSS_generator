   


def check_for_rules (rows):
   
    rows[-1].pop()
    
    valid = False
 # Check downward progression       
    downward_progression = True
    for row in rows:
        print(row)
        for i in range(len(row) - 1): 
            if row[i] <= row[i + 1]:  
                downward_progression = False
                break  # Exit the inner loop if not progressing
        if not downward_progression:
            break  # Exit the outer loop if a non-progressing row is found 
      

# Check upward progression
    upward_progression = True
    for row in rows:
        for i in range(len(row) - 1): 
            if row[i] >= row[i + 1]: #any upward progression, I'm for now ignoring stepsize 
                upward_progression = False
                break  # Exit the inner loop if not progressing
        if not upward_progression:
            break  # Exit the outer loop if a non-progressing row is found
            
            
 #check distribute three
    distribute_three = True
    reference_row = rows[0]

    for row in rows[1:]:
        # Check if all values in row exist in reference_row and are unique in the row
        if not all(value in reference_row for value in row) or len(row) != len(set(row)):
            distribute_three = False
            break
        
    if upward_progression or downward_progression or distribute_three:
        print('l')
        valid = False
        
    else:
        valid = True
        
    return valid

print(check_for_rules(a))