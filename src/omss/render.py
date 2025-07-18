#OMSS imports
from .element import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Line, BigShape, LittleShape, Linenumbers

#general imports
import cv2
import numpy as np
import math
from math import cos, sin, pi



# Global Mapping dictionaries. Basically here we couple the attributes of the enum classes to actual values
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
    Colors.BLUE: (184, 126, 55),      #377eb8 
    Colors.ORANGE: (0, 127, 255),     #ff7f00
    Colors.GREEN: (74, 175, 77),     #4daf4a
    Colors.BROWN: (40, 86, 166),     #a65628
    Colors.PURPLE: (163, 78, 152),     #984ea3
    Colors.GRAY: (153, 153, 153),     #999999
    Colors.RED: (28, 26, 228),     #999999
    Colors.YELLOW: (0, 222, 222)   #dede00
}



NUMBER_MAP = {
   
    Linenumbers.ONE: 1,
    Linenumbers.TWO: 2,
    Linenumbers.THREE: 3,
    Linenumbers.FOUR: 4,
    Linenumbers.FIVE: 5}
    

LINE_SPACING = 30  # Distance between multiple lines


def render_matrix(element_dict,  problem_matrix=False):
    # Settings
    panel_size = 1500
    background_color = (255, 255, 255)
    line_color = (0, 0, 0)
    line_thickness = 5

    # Create a blank canvas with background color
    img = np.ones((panel_size, panel_size, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)

    # Cell size for each grid in the 3x3 matrix
    cell_size = panel_size // 3

    # Dictionary to collect elements by grid position (row, column)
    grouped_elements = {}

    # Collect all elements based on their element_index
    for matrix in element_dict.values():
        for element_list in matrix:  # element_list is a list of elements in the same cell
            for element in element_list:  # Iterate through each element in the list
                if element.element_index is None:  # Skip elements with None as element_index
                    continue

                r, c = element.element_index  # Extract row and column index
                if problem_matrix and (r, c) == (2, 2):  # Skip last cell for problem_matrix
                    continue

                if (r, c) not in grouped_elements:
                    grouped_elements[(r, c)] = []
                grouped_elements[(r, c)].append(element)  # Store elements in the correct grid cell

    # Render the grouped elements into their respective grid cells
    for (r, c), elements in grouped_elements.items():
        element_img = render_element(elements)  # Render all elements in this cell

        # Calculate the position of the current cell
        y_start, x_start = r * cell_size, c * cell_size

        # Place the rendered elements in the corresponding position on the main canvas
        img[y_start:y_start + cell_size, x_start:x_start + cell_size] = element_img

    # Draw grid lines between the cells
    for i in range(1, 3):
        cv2.line(img, (0, i * cell_size), (panel_size, i * cell_size), line_color, line_thickness)
        cv2.line(img, (i * cell_size, 0), (i * cell_size, panel_size), line_color, line_thickness)

  
 
    return img
    

def render_element(elements, idx=None):
    """
    Render multiple elements on a square canvas and return the composite image.
    """
    # some settings
    panel_size = 500
    background_color = (255, 255, 255)
    
    # Create a blank color canvas
    img = np.ones((panel_size, panel_size, 3), np.uint8) * np.array(background_color, dtype=np.uint8)

    # Define size and position adjustments for the elements
    size_factor = {
        Sizes.SMALL: 0.2,
        Sizes.MEDIUM: 0.5,
        Sizes.LARGE: 0.9
    }

    corner_size_multiplier = 0.45
    corner_length_multiplier = 0.4

    position_centers = {
        Positions.TOP_LEFT: (panel_size // 4, panel_size // 4),
        Positions.TOP_RIGHT: (3 * panel_size // 4, panel_size // 4),
        Positions.BOTTOM_LEFT: (panel_size // 4, 3 * panel_size // 4),
        Positions.BOTTOM_RIGHT: (3 * panel_size // 4, 3 * panel_size // 4),
    }

    # Dict that couples shape attributes/line attributes to the drawing function
    shape_renderers = {
        Shapes.TRIANGLE: render_triangle,
        Shapes.SQUARE: render_square,
        Shapes.PENTAGON: render_pentagon,
        Shapes.SEPTAGON: render_septagon,
        Shapes.DECAGON: render_decagon,
        Shapes.CIRCLE: render_circle,
        Linetypes.SOLID: render_straight_line,
        Linetypes.CURVED: render_curved_line,
        Linetypes.WAVED: render_wavy_line
    }

    for element in elements:
        if (hasattr(element, 'linenumber') and (element.linenumber is None or element.linenumber == 0)) or \
         (hasattr(element, 'littleshapenumber') and (element.littleshapenumber is None or element.littleshapenumber == 0)) or \
           (hasattr(element, 'number') and (element.number is None or element.number == 0)):
               
            continue  # Skip rendering

        # Handle multiple positions
        positions = element.position if isinstance(element.position, list) else [element.position]

        for pos in positions:
            center = position_centers.get(pos, (panel_size // 2, panel_size // 2))

            # line
            if isinstance(element, Line):
                length_multiplier = corner_length_multiplier if pos in {
                    Positions.TOP_LEFT, Positions.TOP_RIGHT, Positions.BOTTOM_LEFT, Positions.BOTTOM_RIGHT
                } else 1.0
                length = 300 * length_multiplier
                shape_renderers.get(element.linetype)(img, center, length, element)

            # big shape / little shape
            elif isinstance(element, BigShape) or isinstance(element, LittleShape):
                size_multiplier = corner_size_multiplier if pos in {
                    Positions.TOP_LEFT, Positions.TOP_RIGHT, Positions.BOTTOM_LEFT, Positions.BOTTOM_RIGHT
                } else 1.0
                size = int(size_multiplier * size_factor.get(element.size, 1) * panel_size / 2)
                shape_renderers.get(element.shape)(img, center, size, element)

    return img


    

def render_triangle(img, center, size, element):
    angle = ANGLE_MAP[element.angle] * pi / 180  # Convert angle to radians
    color = COLOR_MAP[element.color]

    scale_factor = 1.8
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



def render_square(img, center, size, element):
    angle = ANGLE_MAP[element.angle] * pi / 180  # Convert angle to radians
    color = COLOR_MAP[element.color]
    
    scale_factor = 1.5
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


def render_pentagon(img, center, size, element):
    color = COLOR_MAP[element.color]    
    angle = ANGLE_MAP[element.angle] * pi / 180  # Convert angle to radians

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


def render_septagon(img, center, size, element):
    color = COLOR_MAP[element.color]  
    angle = ANGLE_MAP[element.angle] * pi / 180  # Convert angle to radians

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



def render_decagon(img, center, size, element):
    color = COLOR_MAP[element.color]
    angle = ANGLE_MAP[element.angle] * pi / 180  # Convert angle to radians

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
    
 


def render_circle(img, center, length, element):
    color = COLOR_MAP[element.color]
    start_angle = ANGLE_MAP[element.angle] + 108 ##we need to offset it  to make the wedge center appear at the bottom, 90 +36/2
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


LINE_SPACING = 30  # Adjust line spacing if needed

def rotate_point(point, center, angle):
    """Rotates a point around a center by a given angle (in radians)."""
    x, y = point
    cx, cy = center
    cos_a, sin_a = cos(angle), sin(angle)

    # Check for 180-degree multiples (to avoid floating-point drift)
    if abs(angle % pi) < 1e-6:  
        return round(2 * cx - x), round(2 * cy - y)

    x_new = cos_a * (x - cx) - sin_a * (y - cy) + cx
    y_new = sin_a * (x - cx) + cos_a * (y - cy) + cy

    return round(x_new), round(y_new)  # Use round() to minimize drift

def draw_arrowhead(img, start, end, color=(0, 0, 0), thickness=3, size=16, forward_offset=6):
    """Draws a clean triangle arrowhead pointing from start to end, slightly ahead of the endpoint."""
    angle = np.arctan2(end[1] - start[1], end[0] - start[0])

    # Shift the whole arrowhead forward
    dx = forward_offset * cos(angle)
    dy = forward_offset * sin(angle)

    tip = (int(end[0] + dx), int(end[1] + dy))
    left = (int(tip[0] - size * cos(angle - pi / 6)),
            int(tip[1] - size * sin(angle - pi / 6)))
    right = (int(tip[0] - size * cos(angle + pi / 6)),
             int(tip[1] - size * sin(angle + pi / 6)))

    pts = np.array([tip, left, right], np.int32)
    cv2.fillConvexPoly(img, pts, color)




def render_straight_line(img, center, length, element):
    """Draws one or multiple straight lines with arrowheads."""
    color = (0, 0, 0)
    thickness = 3
    angle = ANGLE_MAP[element.angle] * pi / 180
    number = NUMBER_MAP[element.linenumber]
    total_offset = (number - 1) * LINE_SPACING // 2

    for i in range(number):
        offset = -total_offset + i * LINE_SPACING
        adjusted_center = (center[0], center[1] + offset)
        start = (adjusted_center[0] - length // 2, adjusted_center[1])
        end = (adjusted_center[0] + length // 2, adjusted_center[1])

        start = rotate_point(start, center, angle)
        end = rotate_point(end, center, angle)

        cv2.line(img, start, end, color, thickness)
        draw_arrowhead(img, start, end, color, thickness)


def render_curved_line(img, center, length, element):
    """Draws one or multiple curved lines with arrowheads."""
    color = (0, 0, 0)
    thickness = 3
    angle = ANGLE_MAP[element.angle] * pi / 180
    number = NUMBER_MAP[element.linenumber]
    total_offset = (number - 1) * LINE_SPACING // 2

    for i in range(number):
        offset = -total_offset + i * LINE_SPACING
        adjusted_center = (center[0], center[1] + offset)
        start = (adjusted_center[0] - length // 2, adjusted_center[1])
        end = (adjusted_center[0] + length // 2, adjusted_center[1])
        control = (adjusted_center[0], adjusted_center[1] - length // 3)

        curve_points = []
        for t in np.linspace(0, 1, 100):
            x = int((1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0])
            y = int((1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1])
            curve_points.append((x, y))

        curve_points = [rotate_point(pt, center, angle) for pt in curve_points]
        cv2.polylines(img, [np.array(curve_points)], isClosed=False, color=color, thickness=thickness)

        if len(curve_points) >= 2:
            draw_arrowhead(img, curve_points[-2], curve_points[-1], color, thickness)


def render_wavy_line(img, center, length, element, amplitude=10, frequency=3):
    """Draws one or multiple wavy lines with arrowheads."""
    color = (0, 0, 0)
    thickness = 3
    angle = ANGLE_MAP[element.angle] * pi / 180
    number = NUMBER_MAP[element.linenumber]
    total_offset = (number - 1) * LINE_SPACING // 2

    for i in range(number):
        offset = -total_offset + i * LINE_SPACING
        adjusted_center = (center[0], center[1] + offset)
        start_x = adjusted_center[0] - length // 2
        end_x = adjusted_center[0] + length // 2

        wave_points = []
        for x in np.linspace(start_x, end_x, 100):
            y = adjusted_center[1] + amplitude * sin(frequency * (x - start_x) * 2 * pi / length)
            wave_points.append((int(x), int(y)))

        wave_points = [rotate_point(pt, center, angle) for pt in wave_points]
        cv2.polylines(img, [np.array(wave_points)], isClosed=False, color=color, thickness=thickness)

        if len(wave_points) >= 2:
            draw_arrowhead(img, wave_points[-2], wave_points[-1], color, thickness)


#this map is no longer used but the colours looked so damn good
#ORIGINAL_COLOR_MAP = {
  #    Colors.RED: (100, 60, 180),       # Softer Red V
  #    Colors.PINK: (180, 140, 255),     # Pink V
   #   Colors.GREEN: (90, 200, 100),     # Soft Green V
   #   Colors.YELLOW: (0, 230, 255),     # Mellow Yellow V
   #   Colors.BLUE: (180, 160, 120),     # Blue
   #   Colors.LAVENDER: (230, 130, 190),     # Lavender
   #   Colors.BROWN: (100, 180, 180),     # brown
   #   Colors.ORANGE: (100, 160, 255)   #teal
#  }
