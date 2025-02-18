import cv2
import numpy as np
import math
from math import cos, sin, pi
from entity import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linelengths, Linewidths, Line, BigShape, LittleShape, Linenumbers

def render_matrix(entity_dict, panel_size=1500, background_color=(255, 255, 255), line_color=(0, 0, 0), line_thickness=5):
    """
    Render corresponding entities from multiple 3x3 matrices together in each grid cell.
    
    Args:
        entity_dict: A dictionary where keys are entity types and values are 3x3 matrices of entities.
        panel_size: Size of the entire grid panel in pixels (square).
        background_color: Background color as an RGB tuple.
        line_color: Color of the lines between cells in BGR format.
        line_thickness: Thickness of the grid lines.
    
    Returns:
        Composite grid image with lines as a NumPy array.
    """
    # Create a blank canvas with background color
    img = np.ones((panel_size, panel_size, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)

    # Cell size for each grid in the 3x3 matrix (e.g., 500x500 for a 1500x1500 panel)
    cell_size = panel_size // 3

    # Render the grid for all entities
    for r in range(3):  # Loop over rows
        for c in range(3):  # Loop over columns
            # Collect entities from each matrix at the current position
            entities = [matrix[r][c] for matrix in entity_dict.values()]

            # Render the entities together (fit within each cell of the grid)
            entity_img = render_entity(entities, panel_size=cell_size, background_color=background_color)

            # Calculate the position of the current cell
            y_start, x_start = r * cell_size, c * cell_size

            # Place the rendered entities on the main canvas
            img[y_start:y_start + cell_size, x_start:x_start + cell_size] = entity_img

    # Draw grid lines between the cells
    for i in range(1, 3):
        cv2.line(img, (0, i * cell_size), (panel_size, i * cell_size), line_color, line_thickness)
        cv2.line(img, (i * cell_size, 0), (i * cell_size, panel_size), line_color, line_thickness)

    # Return the composite image
    return img

# Global Maps
ANGLE_MAP = {
    Angles.ZERO: 0,
    Angles.THIRTY_SIX: 36,
    Angles.SEVENTY_TWO: 72,
    Angles.ONE_HUNDRED_EIGHT: 108,
    Angles.ONE_FORTY_FOUR: 144,
    Angles.ONE_EIGHTY: 180,
    Angles.TWO_SIXTEEN: 216,
    Angles.TWO_FIFTY_TWO: 252,
    Angles.TWO_EIGHTY_EIGHT: 288,
    Angles.THREE_TWENTY_FOUR: 324,
}

COLOR_MAP = {
    Colors.RED: (100, 60, 180),       # Softer Red
    Colors.BLUE: (180, 140, 255),     # Soft Sky Blue
    Colors.GREEN: (90, 200, 100),     # Soft Green
    Colors.YELLOW: (200, 180, 120),   # Mellow Yellow
    Colors.LAVENDER: (180, 130, 250), # Soft Lavender
    Colors.ORANGE: (220, 120, 80),    # Muted Orange
    Colors.PINK: (230, 130, 190),     # Softer Pink
    Colors.BEIGE: (180, 160, 120),    # Beige
    Colors.TEAL: (100, 180, 180),     # Teal
}


NUMBER_MAP = {
    Linenumbers.ONE: 1,
    Linenumbers.TWO: 2,
    Linenumbers.THREE: 3}

    
LINEWIDTH_MAP = {
        Linewidths.THIN: 3,
        Linewidths.MEDIUM: 5,
        Linewidths.THICK: 7
    }
LINE_SPACING = 30  # Distance between multiple lines

def render_alternatives (entities, panel_size=500, background_color=(255, 255, 255)):
    """
    Render multiple entities together in a single grid and return the image.
    
    Args:
        entities: A list of entity objects to be drawn.
        panel_size: Size of the square canvas.
        background_color: Background color as an RGB tuple.
    
    Returns:
        A NumPy array representing the image.
    """
    print('a', entities)
    # Create a blank canvas
    img = np.ones((panel_size, panel_size, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)

    # Use the existing function to render the entities
    img = render_entity(entities, panel_size=panel_size, background_color=background_color)

    return img


def render_entity(entities, panel_size=500, background_color=(255, 255, 255)):
    """
    Render multiple entities on a square canvas and return the composite image.
    """
    # Create a blank color canvas
    img = np.ones((panel_size, panel_size, 3), np.uint8) * np.array(background_color, dtype=np.uint8)

    # Define size and position adjustments
    size_factor = {
        Sizes.SMALL: 0.3,
        Sizes.MEDIUM: 0.5,
        Sizes.LARGE: 0.9
    }

    length_factor = {
        Linelengths.SHORT: 0.6,
        Linelengths.MEDIUM: 1.0,
        Linelengths.LONG: 1.4
    }

    corner_size_multiplier = 0.45
    corner_length_multiplier = 0.6

    position_centers = {
        Positions.TOP_LEFT: (panel_size // 4, panel_size // 4),
        Positions.TOP_RIGHT: (3 * panel_size // 4, panel_size // 4),
        Positions.BOTTOM_LEFT: (panel_size // 4, 3 * panel_size // 4),
        Positions.BOTTOM_RIGHT: (3 * panel_size // 4, 3 * panel_size // 4),
    }

    shape_renderers = {
        Shapes.TRIANGLE: render_triangle,
        Shapes.SQUARE: render_square,
        Shapes.PENTAGON: render_pentagon,
        Shapes.SEPTAGON: render_septagon,
        Shapes.DECAGON: render_decagon,
        Shapes.CIRCLE: render_circle,
        Linetypes.SOLID: render_solid_line,
        Linetypes.DASHED: render_dashed_line,
        Linetypes.LARGEDASHED: render_large_dashed_line
    }

    for entity in entities:
        center = position_centers.get(entity.position, (panel_size // 2, panel_size // 2)) if entity.position else (panel_size // 2, panel_size // 2)
             
        

        if isinstance(entity, Line):            
            length_multiplier = corner_length_multiplier if entity.position in {
                Positions.TOP_LEFT, Positions.TOP_RIGHT, Positions.BOTTOM_LEFT, Positions.BOTTOM_RIGHT
            } else 1.0
            length = int(length_multiplier * length_factor.get(entity.linelength, 1) * panel_size / 2)
            print(length_factor.get(entity.linelength, 1) )
            shape_renderers.get(entity.linetype)(img, center, length, entity)

        elif isinstance(entity, BigShape) or isinstance (entity, LittleShape):
            size_multiplier = corner_size_multiplier if entity.position in {
                Positions.TOP_LEFT, Positions.TOP_RIGHT, Positions.BOTTOM_LEFT, Positions.BOTTOM_RIGHT
            } else 1.0
            size = int(size_multiplier * size_factor.get(entity.size, 1) * panel_size / 2)
            shape_renderers.get(entity.shape)(img, center, size, entity)

    return img

    

def render_triangle(img, center, size, entity):
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert angle to radians
    color = COLOR_MAP[entity.color]

    scale_factor = 1.7
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2
    height = adjusted_size * np.sqrt(3) / 2

    # Define main triangle points
    C1 = [0, -2 * height / 3]  # Top vertex
    C2 = [-half_size, height / 3]  # Bottom-left vertex
    C3 = [half_size, height / 3]  # Bottom-right vertex

    # Define cutout wedge points
    wedge_size = adjusted_size / 3
    wedge_size = wedge_size * 0.5# Adjust the size of the missing wedge
    wedge_height = wedge_size * np.sqrt(3) / 2  # Height of the wedge

    C4 = [-wedge_size / 2, height / 3]  # Left edge of wedge
    C5 = [0, height / 3 - wedge_height]  # Bottom tip of wedge, cv2 0.0 is top left corner so smaller y means going up
    C6 = [wedge_size / 2, height / 3]  # Right edge of wedge

    # Create the ordered list of points to form the correct shape
    pts = np.array([
        C1,  # Top vertex
        C2,  # Bottom-left vertex
        C4,  # Left edge of wedge
        C5,  # Bottom tip of wedge
        C6,  # Right edge of wedge
        C3   # Bottom-right vertex
    ], np.float32)

    # Apply rotation 
    rotation_matrix = np.array([
        [cos(+angle), -sin(+angle)],
        [sin(+angle), cos(+angle)]
    ])

    rotated_pts = np.dot(pts, rotation_matrix.T) + center  # Rotate and shift to center

    # Convert to integer points for OpenCV
    rotated_pts = rotated_pts.astype(np.int32)

    # Draw the modified triangle
    cv2.fillPoly(img, [rotated_pts], color)
    
    # Outline for visibility
    cv2.polylines(img, [rotated_pts], isClosed=True, color=(0, 0, 0), thickness=2)



def render_square(img, center, size, entity):
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert angle to radians
    color = COLOR_MAP[entity.color]
    
    scale_factor = 1.3
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2
    
    # Define the square points 
    C1 = [center[0] - half_size, center[1] - half_size]  # Top-left corner
    C2 = [center[0] + half_size, center[1] - half_size]  # Top-right corner
    C3 = [center[0] + half_size, center[1] + half_size]  # Bottom-right corner
    C4 = [center[0] - half_size, center[1] + half_size]  # Bottom-left corner
        
    
    # Define the wedge points 
    wedge_size = adjusted_size / 4    
    wedge_height = wedge_size * np.sqrt(3) / 2  # Height of the wedge
    
    C5 = [center[0] + wedge_size / 2, center[1] + half_size]  # Bottom-right corner of wedge
    C6 = [center[0], center[1] + half_size - wedge_height]  # Tip of the wedge, cv2 0.0 is in top lef corner, so small y values means going up
    C7 = [center[0] -  wedge_size / 2, center[1] + half_size]  # Bottom-left corner of wedge
    
    # Combine the points for the square and wedge
    pts = np.array([C1, #topleft corner
                    C2, #top right corner
                    C3, #bottom right corner
                    C5, #bottom right corner of wedge
                    C6, #tip of wedge
                    C7, # bottom left corner of wedge
                    C4]  , np.int32)#bottom left corner

    # Apply rotation manually
    rotation_matrix = np.array([
        [cos(+angle), -sin(+angle)],
        [sin(+angle), cos(+angle)]
    ])

    # Calculate the center shift and apply rotation
    shifted_pts = np.dot(pts - np.array(center), rotation_matrix.T) + center

    # Convert to integer points for OpenCV
    shifted_pts = shifted_pts.astype(np.int32)

    # Draw the modified square with the triangle cutout
    cv2.fillPoly(img, [shifted_pts], color)

    # Outline for visibility
    cv2.polylines(img, [shifted_pts], isClosed=True, color=(0, 0, 0), thickness=2)


def render_pentagon(img, center, size, entity):
    color = COLOR_MAP[entity.color]    
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert angle to radians

    # Standard orientation: C1 at the top
    base_angle = -pi / 2  

    # Step 1: Define initial (unrotated) pentagon points
    C1 = [size * cos(base_angle + 2 * pi * 0 / 5), size * sin(base_angle + 2 * pi * 0 / 5)]
    C2 = [size * cos(base_angle + 2 * pi * 1 / 5), size * sin(base_angle + 2 * pi * 1 / 5)]
    C3 = [size * cos(base_angle + 2 * pi * 2 / 5), size * sin(base_angle + 2 * pi * 2 / 5)]
    C4 = [size * cos(base_angle + 2 * pi * 3 / 5), size * sin(base_angle + 2 * pi * 3 / 5)]
    C5 = [size * cos(base_angle + 2 * pi * 4 / 5), size * sin(base_angle + 2 * pi * 4 / 5)]

    # Step 2: Define additional wedge points  
    wedge_height = size * 0.25  # How far up the wedge extends  
    bottom_offset = size * 0.5 # Distance between C6/C8 and C3/C4
    
    # C6 and C8 are closer to the center, between C3 and C4
    C6 =  [C3[0] - bottom_offset, C4[1]] # C6 is closer to C3
    C8 = [C4[0] + bottom_offset, C4[1]]  # C8 is closer to C4
       
    # C7 is above the midpoint between C6 and C8, extending upwards
    C7 = [(C6[0] + C8[0]) / 2, C6[1] - wedge_height]  # For some reason I have to substract the wedge-height in order to go up, seems like the coordinate system is reversed? aah 0.0 is top left in cv2
    
    # Step 3: Store all points in order (forming a single shape)
    pts = np.array([C1, C2, C3, C6, C7, C8, C4, C5], dtype=np.float32)
 
    # Step 4: Create the rotation matrix
    rotation_matrix = np.array([
        [cos(angle), -sin(angle)],
        [sin(angle), cos(angle)]
    ])

    # Step 5: Apply rotation to all points
    rotated_pts = np.dot(pts, rotation_matrix.T)

    # Step 6: Translate points to the center
    pts_final = np.round(rotated_pts + center).astype(np.int32)

    # Step 7: Draw filled pentagon with wedge integrated
    cv2.fillPoly(img, [pts_final.reshape((-1, 1, 2))], color)

    # Step 8: Draw outline
    cv2.polylines(img, [pts_final.reshape((-1, 1, 2))], isClosed=True, color=(0, 0, 0), thickness=2)


def render_septagon(img, center, size, entity):
    color = COLOR_MAP[entity.color]  
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert angle to radians

    # Standard orientation: C1 at the top
    base_angle = -pi / 2  

    # Step 1: Define initial (unrotated) septagon points
    C1 = [size * cos(base_angle + 2 * pi * 0 / 7), size * sin(base_angle + 2 * pi * 0 / 7)]
    C2 = [size * cos(base_angle + 2 * pi * 1 / 7), size * sin(base_angle + 2 * pi * 1 / 7)]
    C3 = [size * cos(base_angle + 2 * pi * 2 / 7), size * sin(base_angle + 2 * pi * 2 / 7)]
    C4 = [size * cos(base_angle + 2 * pi * 3 / 7), size * sin(base_angle + 2 * pi * 3 / 7)]
    C5 = [size * cos(base_angle + 2 * pi * 4 / 7), size * sin(base_angle + 2 * pi * 4 / 7)]
    C6 = [size * cos(base_angle + 2 * pi * 5 / 7), size * sin(base_angle + 2 * pi * 5 / 7)]
    C7 = [size * cos(base_angle + 2 * pi * 6 / 7), size * sin(base_angle + 2 * pi * 6 / 7)]

    # Step 2: Define additional w
    wedge_height = size * 0.25  # How far up the wedge extends  
    bottom_offset = size * 0.30 # Distance between C8/C9 and C4/C5
    
    # C8 and C9 are closer to the center, between C4 and C5
    C8 = [C4[0] - bottom_offset, C4[1]] # C8 is closer to C4
    C9 = [C5[0] + bottom_offset, C4[1]]  #  C9 is closer to C5  
 
    
    # C10 is above the midpoint between C8 and C9, extending upwards
    C10 = [(C8[0] + C9[0]) / 2, C8[1] - wedge_height]  

    # Step 3: Store all points in order (forming a single shape)
    pts = np.array([C1, C2, C3, C4, C8, C10, C9, C5, C6, C7], dtype=np.float32)

    # Step 4: Create the rotation matrix
    rotation_matrix = np.array([
        [cos(angle), -sin(angle)],
        [sin(angle), cos(angle)]
    ])

    # Step 5: Apply rotation to all points
    rotated_pts = np.dot(pts, rotation_matrix.T)

    # Step 6: Translate points to the center
    pts_final = np.round(rotated_pts + center).astype(np.int32)

    # Step 7: Draw filled septagon with wedge integrated
    cv2.fillPoly(img, [pts_final.reshape((-1, 1, 2))], color)

    # Step 8: Draw outline
    cv2.polylines(img, [pts_final.reshape((-1, 1, 2))], isClosed=True, color=(0, 0, 0), thickness=2)



def render_decagon(img, center, size, entity):
    color = COLOR_MAP[entity.color]
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert angle to radians

    # Shift the starting angle to a different point on the decagon
    base_angle = 0  # Set this to any angle you prefer to shift the shape's orientation

    # Step 1: Define initial (unrotated) decagon points
    C1 = [size * cos(base_angle + 2 * pi * 0 / 10), size * sin(base_angle + 2 * pi * 0 / 10)]
    C2 = [size * cos(base_angle + 2 * pi * 1 / 10), size * sin(base_angle + 2 * pi * 1 / 10)]
    C3 = [size * cos(base_angle + 2 * pi * 2 / 10), size * sin(base_angle + 2 * pi * 2 / 10)]
    C4 = [size * cos(base_angle + 2 * pi * 3 / 10), size * sin(base_angle + 2 * pi * 3 / 10)]
    C5 = [size * cos(base_angle + 2 * pi * 4 / 10), size * sin(base_angle + 2 * pi * 4 / 10)]
    C6 = [size * cos(base_angle + 2 * pi * 5 / 10), size * sin(base_angle + 2 * pi * 5 / 10)]
    C7 = [size * cos(base_angle + 2 * pi * 6 / 10), size * sin(base_angle + 2 * pi * 6 / 10)]
    C8 = [size * cos(base_angle + 2 * pi * 7 / 10), size * sin(base_angle + 2 * pi * 7 / 10)]
    C9 = [size * cos(base_angle + 2 * pi * 8 / 10), size * sin(base_angle + 2 * pi * 8 / 10)]
    C10 = [size * cos(base_angle + 2 * pi * 9 / 10), size * sin(base_angle + 2 * pi * 9 / 10)]

    # Step 2: Define additional wedge points (same concept as previous)
    wedge_height = size * 0.25  # How far up the wedge extends  
    bottom_offset = size * 0.40  # Distance between C6/C7 and C4/C5
    
    # C11 and C12 are closer to the center, between C9 and C8
    C11 =  [C8[0] + bottom_offset, C4[1]]  # C11 is closer to C5
    C12 =  [C9[0] - bottom_offset, C4[1]]# C12 is closer to C4
       
    
    # C13 is above the midpoint between C11 and C12, extending upwards
    C13 = [(C11[0] + C12[0]) / 2, C11[1] - wedge_height]  

    # Step 3: Store all points in order (forming a single shape)
    pts = np.array([C1, C2, C3, C11, C13, C12, C4, C5, C6,C7,C8, C9, C10], dtype=np.float32)

    # Step 4: Create the rotation matrix
    rotation_matrix = np.array([
        [cos(angle), -sin(angle)],
        [sin(angle), cos(angle)]
    ])

    # Step 5: Apply rotation to all points
    rotated_pts = np.dot(pts, rotation_matrix.T)

    # Step 6: Translate points to the center
    pts_final = np.round(rotated_pts + center).astype(np.int32)

    # Step 7: Draw filled decagon with wedge integrated
    cv2.fillPoly(img, [pts_final.reshape((-1, 1, 2))], color)

    # Step 8: Draw outline
    cv2.polylines(img, [pts_final.reshape((-1, 1, 2))], isClosed=True, color=(0, 0, 0), thickness=2)
    
 


def render_circle(img, center, length, entity):
    color = COLOR_MAP[entity.color]
    start_angle = ANGLE_MAP[entity.angle] + 108 ##we need to offset it  to make the wedge center appear at the bottom, 90 +36/2
    end_angle = start_angle + 324  # 360 - 36

    # Draw the filled arc
    cv2.ellipse(img, center, (int(length), int(length)), 0, start_angle, end_angle, color, -1)

    # Calculate the start and end points for the missing pie section
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)

    start_point = (int(center[0] + length * math.cos(start_rad)), int(center[1] + length * math.sin(start_rad)))
    end_point = (int(center[0] + length * math.cos(end_rad)), int(center[1] + length * math.sin(end_rad)))

    # Draw the outer arc
    cv2.ellipse(img, center, (int(length), int(length)), 0, start_angle, end_angle, (0, 0, 0), 2)

    # Draw the missing pie edges (lines from center to the arc)
    cv2.line(img, center, start_point, (0, 0, 0), 2)
    cv2.line(img, center, end_point, (0, 0, 0), 2)



    


# Line Rendering Functions
def rotate_point(point, center, angle):#needed for the lines
    """
    Rotates a point around a center by a given angle in radians.
    """
    px, py = point
    cx, cy = center
    s, c = sin(angle), cos(angle)
    # Translate point back to origin:
    px -= cx
    py -= cy
    # Rotate point:
    x_new = px * c - py * s
    y_new = px * s + py * c
    # Translate point back:
    px = x_new + cx
    py = y_new + cy
    return int(px), int(py)



def render_solid_line(img, center, length, entity):
    """
    Renders one or multiple solid lines with rotation based on entity.angle.
    """
    color = (0, 0, 0)  # Default black color
    thickness = LINEWIDTH_MAP.get(entity.linewidth, 1)
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert to radians
    number = NUMBER_MAP[entity.linenumber]  # Get the number of lines to draw
    
    # Calculate vertical offsets for multiple lines
    total_offset = (number - 1) * LINE_SPACING // 2
    
    for i in range(number):
        offset = -total_offset + i * LINE_SPACING
        
        # Adjust center for the current line
        adjusted_center = (center[0], center[1] + offset)
        
        # Calculate unrotated start and end points
        line_start = (adjusted_center[0] - length // 2, adjusted_center[1])
        line_end = (adjusted_center[0] + length // 2, adjusted_center[1])
        
        # Rotate points around the center
        line_start = rotate_point(line_start, center, angle)
        line_end = rotate_point(line_end, center, angle)
        
        # Draw the rotated line
        cv2.line(img, line_start, line_end, color, thickness)

def render_dashed_line(img, center, length, entity, gap_multiplier=1):
    """
    Renders one or multiple dashed lines with rotation based on entity.angle.
    """
    color = (0, 0, 0)  # Default black color
    thickness = LINEWIDTH_MAP.get(entity.linewidth, 1)
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert to radians
    number = NUMBER_MAP[entity.linenumber]  # Get the number of lines to draw
    dash_length = length // 10
    gap_length = dash_length * gap_multiplier
    
    # Calculate vertical offsets for multiple lines
    total_offset = (number - 1) * LINE_SPACING // 2
    
    for i in range(number):
        offset = -total_offset + i * LINE_SPACING
        adjusted_center = (center[0], center[1] + offset)
        
        # Generate dashes for the current line
        line_start_x = adjusted_center[0] - length // 2
        line_end_x = adjusted_center[0] + length // 2
        dashes = []
        
        for start_x in range(line_start_x, line_end_x, dash_length + gap_length):
            dash_end_x = min(start_x + dash_length, line_end_x)  # Ensure it doesn't overshoot
            dash_start = (start_x, adjusted_center[1])
            dash_end = (dash_end_x, adjusted_center[1])
            dashes.append((dash_start, dash_end))
        
        # Rotate and draw each dash
        for dash_start, dash_end in dashes:
            dash_start = rotate_point(dash_start, center, angle)
            dash_end = rotate_point(dash_end, center, angle)
            cv2.line(img, dash_start, dash_end, color, thickness)

def render_large_dashed_line(img, center, length, entity):
    """
    Renders one or multiple dashed lines with larger gaps and rotation based on entity.angle.
    """
    render_dashed_line(img, center, length, entity, gap_multiplier=3)



