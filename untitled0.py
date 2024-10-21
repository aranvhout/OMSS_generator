numerical_matrix = [
       # Downward progression
        # Downward progression
       # Not downward progression
    [3, 2, 1],    # Downward progression
    [9, 9],    # Not downward progression
]
downward_progression = True
for row in numerical_matrix:
    for i in range(len(row) - 1):  # Loop through indices of the row
        if row[i] <= row[i + 1]:  # Check for strictly decreasing
            downward_progression = False
            print(row)
            break  # Exit the inner loop if not progressing
    if not downward_progression:  # Corrected to check downward_progression
        break  # Exit the outer loop if a non-progressing row is found
