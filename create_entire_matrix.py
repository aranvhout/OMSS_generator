from entity import create_random_entity, Entity



seed_list=[0,1,2,3,4,5,6,7,8,9]
def create_starting_matrix(n_rows=3, n_columns=3, seed_list=None, z=None):
    if z is not None:  # 3D matrix case
        matrix = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                depth = []
                for k in range(z):
                    depth.append(create_random_entity(seed_list))
                row.append(depth)
            matrix.append(row)
            
    else:  # 2D matrix case
        matrix = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                entity, seed_list = create_random_entity(seed_list)
                row.append(entity)
                print(seed_list)
            matrix.append(row)
    
    return matrix

matrix=create_starting_matrix(3,3,seed_list)


a =  True
if a is True:
    for row_index, row in enumerate(matrix):
        print(f"\nRow {row_index + 1}:")
        for i, entity in enumerate(row):
            print(f"  Entity {i + 1}: Shape={entity.shape}, Size={entity.size}, Color={entity.color}, Angle={entity.angle}, Index={entity.index}")
