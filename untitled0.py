numerical_matrix = [[3, 2, 1], [3, 2, 1], [4, 1]]

distribute_three = True
reference_row = numerical_matrix[0]

for row in numerical_matrix[1:]:
    # Check if all values in row exist in reference_row and are unique in the row
    if not all(value in reference_row for value in row) or len(row) != len(set(row)):
        distribute_three = False
        break

print(distribute_three)
