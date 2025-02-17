def render_complicated_shape (img, center, size, entity):
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Ensure this is returning correct angles
    print(f"Rotation angle in radians: {angle}")  # Debugging line

    color = COLOR_MAP[entity.color]

    scale_factor = 1.7
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2
    height = adjusted_size * np.sqrt(3) / 2

    # Main triangle points
    pts = np.array([
        [0, -2 * height / 3],  # Top vertex
        [-half_size, height / 3],  # Bottom-left vertex
        [half_size, height / 3],  # Bottom-right vertex
    ], np.float32)

    # Wedge (cutout) triangle points - Adjust the position as needed
    wedge_size = adjusted_size / 3  # Adjust size of the missing wedge
    wedge_height = wedge_size * np.sqrt(3) / 2  # Height of the wedge

    wedge_pts = np.array([
        [0, height / 3],  # Top of the wedge (inside the main triangle)
        [-wedge_size / 2, height / 3 + wedge_height],  # Bottom-left of the wedge
        [wedge_size / 2, height / 3 + wedge_height],  # Bottom-right of the wedge
        ], np.float32)

    # Combine all points
    all_pts = np.vstack([pts, wedge_pts])

    # Apply rotation manually
    rotation_matrix = np.array([
        [cos(-angle), -sin(-angle)],
        [sin(-angle), cos(-angle)]
    ])

    rotated_pts = np.dot(all_pts, rotation_matrix.T) + center  # Rotate and shift to center
    

    # Convert to integer points for OpenCV
    rotated_pts = rotated_pts.astype(np.int32)
   
    # Draw the modified triangle
    cv2.fillPoly(img, [rotated_pts], color)
    

    

    cv2.polylines(img, [rotated_pts], isClosed=True, color=(0, 0, 0), thickness=2)
    
    
    
#old triangle approach
def render_triangle2(img, center, size, entity):
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Ensure this is returning correct angles
    print(f"Rotation angle in radians: {angle}")  # Debugging line

    color = COLOR_MAP[entity.color]

    scale_factor = 1.7
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2
    height = adjusted_size * np.sqrt(3) / 2

    # Define original triangle points (relative to the center)
    pts = np.array([
        [0, -2 * height / 3],  # Top vertex
        [-half_size, height / 3],  # Bottom-left vertex
        [half_size, height / 3],  # Bottom-right vertex
    ], np.float32)

    # Define wedge points
    wedge_size = adjusted_size * 0.15  # Adjust for bigger/smaller cut
    wedge_pts = np.array([
        [0, height / 3 - wedge_size],  # Raised middle-bottom point
        [-wedge_size / 2, height / 3],  # Left bottom edge
        [wedge_size / 2, height / 3],  # Right bottom edge
    ], np.float32)

    # Apply rotation manually
    rotation_matrix = np.array([
        [cos(-angle), -sin(-angle)],
        [sin(-angle), cos(-angle)]
    ])

    rotated_pts = np.dot(pts, rotation_matrix.T) + center  # Rotate and shift to center
    rotated_wedge_pts = np.dot(wedge_pts, rotation_matrix.T) + center  # Rotate and shift

    # Convert to integer points for OpenCV
    rotated_pts = rotated_pts.astype(np.int32)
    rotated_wedge_pts = rotated_wedge_pts.astype(np.int32)

    # Draw the modified triangle
    cv2.fillPoly(img, [rotated_pts], color)
    cv2.fillPoly(img, [rotated_wedge_pts], (255, 255, 255), lineType=cv2.LINE_AA)  # Cutout

    # Create new outline
    new_outline = np.array([
        rotated_pts[0],  # Top vertex
        rotated_pts[1],  # Bottom-left vertex
        rotated_wedge_pts[1],  # Left cut-out
        rotated_wedge_pts[0],  # Middle cut-out point
        rotated_wedge_pts[2],  # Right cut-out
        rotated_pts[2]  # Bottom-right vertex
    ], np.int32)

    cv2.polylines(img, [new_outline], isClosed=True, color=(0, 0, 0), thickness=2)


    
    
    #cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 0), thickness=2)  # Outline
    
def render_square(img, center, size, entity):
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert angle to radians
    print(f"Rotation angle in radians: {angle}")  # Debugging line

    color = COLOR_MAP[entity.color]

    scale_factor = 1.7
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2

    # Define square points (C1, C2, C3, C7 are the corners)
    C1 = [-half_size, -half_size]  # Top-left corner
    C2 = [half_size, -half_size]  # Top-right corner
    C3 = [-half_size, half_size]  # Bottom-left corner
    C7 = [half_size, half_size]  # Bottom-right corner

    # Define the small triangle points (C4, C5, C6 are for the triangle cutout)
    triangle_size = adjusted_size / 3
    triangle_height = triangle_size * np.sqrt(3) / 2  # Height of the triangle

    C4 = [0, half_size - triangle_height]  # Top tip of triangle (C4)
    C5 = [-triangle_size / 2, half_size]  # Left corner of triangle (C5)
    C6 = [triangle_size / 2, half_size]  # Right corner of triangle (C6)

    # Create the ordered list of points to form the square with triangle cutout
    pts = np.array([
        C1,  # Top-left corner
        C2,  # Top-right corner
        C3,  # Bottom-left corner
        C7,  # Bottom-right corner
        C6,  # Right corner of the triangle
        C5,  # Left corner of the triangle
        C4   # Top tip of the triangle
    ], np.float32)

    # Apply rotation manually
    rotation_matrix = np.array([
        [cos(-angle), -sin(-angle)],
        [sin(-angle), cos(-angle)]
    ])

    # Rotate square corners (C1, C2, C3, C7)
    square_pts = np.array([C1, C2, C3, C7], np.float32)
    rotated_square_pts = np.dot(square_pts, rotation_matrix.T) + center

    # Rotate triangle corners (C4, C5, C6)
    triangle_pts = np.array([C4, C5, C6], np.float32)
    rotated_triangle_pts = np.dot(triangle_pts, rotation_matrix.T) + center

    # Combine rotated points (square + triangle)
    rotated_pts = np.vstack([rotated_square_pts, rotated_triangle_pts])

    # Convert to integer points for OpenCV
    rotated_pts = rotated_pts.astype(np.int32)

    # Draw the modified shape (square with a triangle cutout)
    cv2.fillPoly(img, [rotated_pts], color)
    
    # Outline for visibility
    cv2.polylines(img, [rotated_pts], isClosed=True, color=(0, 0, 0), thickness=2)

def render_circle(img, center, length, entity):
    color = COLOR_MAP[entity.color]
    start_angle = ANGLE_MAP[entity.angle] 
    end_angle = 360 - start_angle
    
    cv2.circle(img, center, int(length), color, -1)
    cv2.circle(img, center, int(length), (0, 0, 0), 2)  # Outline
    
    
    cv2.ellipse(img, center, (int(length), int(length)), 0, start_angle, end_angle, (0, 0, 0), -1)

    # Draw the outline of the arc
    cv2.ellipse(img, center, (int(length), int(length)), 0, 0, 180, (0, 0, 0), 2)
