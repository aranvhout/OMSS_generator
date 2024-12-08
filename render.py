import cv2
import numpy as np
from math import cos, sin, pi
from entity import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linewidths, Line, BigShape

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

# Map line widths to numerical values
linewidth_map = {
    Linewidths.THIN: 1,
    Linewidths.MEDIUM: 3,
    Linewidths.THICK: 5
}
def render_entity(entities, panel_size=500, background_color=(255, 255, 255)):
    """
    Render multiple entities on a square canvas and return the composite image.
    
    Args:
        entities: A list of entity objects to render.
        panel_size: Size of the canvas.
        background_color: Background color of the canvas.
    
    Returns:
        A NumPy array representing the composite image with all entities rendered.
    """
   
    # Map angles to numerical values
    angle_map = {
        Angles.ZERO: 0,
        Angles.TWENTY: 20,
        Angles.FORTY: 40,
        Angles.SIXTY: 60,
        Angles.EIGHTY: 80,
        Angles.HUNDRED: 100,
        Angles.ONE_TWENTY: 120,
        Angles.ONE_FORTY: 140,
        Angles.ONE_SIXTY: 160,
    }

   

    
    # Create a blank color canvas (3 channels for RGB)
    img = np.ones((panel_size, panel_size, 3), np.uint8) * np.array(background_color, dtype=np.uint8)

    # Define size and position adjustments for various entities
    size_factor = {
        Sizes.SMALL: 0.3,
        Sizes.MEDIUM: 0.5,
        Sizes.LARGE: 0.9
    }
    corner_size_multiplier = 0.45

    quarter_size = panel_size // 2
    position_centers = {
        Positions.TOP_LEFT: (quarter_size // 2, quarter_size // 2),
        Positions.TOP_RIGHT: (3 * quarter_size // 2, quarter_size // 2),
        Positions.BOTTOM_LEFT: (quarter_size // 2, 3 * quarter_size // 2),
        Positions.BOTTOM_RIGHT: (3 * quarter_size // 2, 3 * quarter_size // 2),
    }

    # Shape rendering functions mapping
    shape_renderers = {
        Shapes.TRIANGLE: render_triangle,
        Shapes.SQUARE: render_square,
        Shapes.PENTAGON: render_pentagon,
        Shapes.HEXAGON: render_hexagon,
        Shapes.DECAGON: render_decagon,
        Shapes.CIRCLE: render_circle,
        Linetypes.SOLID: render_solid_line,
        Linetypes.DASHED: render_dashed_line,
        Linetypes.DOTTED: render_dotted_line
    }

    # Loop through each entity and render it
    for entity in entities:
        # If position is None, set it to center
        if entity.position is None:
            center = (panel_size // 2, panel_size // 2)  # Center of the grid
        else:
            center = position_centers.get(entity.position, (panel_size // 2, panel_size // 2))  # Default to center if not found
        
        # Determine size of entity
        size_multiplier = corner_size_multiplier if entity.position in {
            Positions.TOP_LEFT, Positions.TOP_RIGHT, Positions.BOTTOM_LEFT, Positions.BOTTOM_RIGHT
        } else 1.0
        size = int(size_multiplier * size_factor[entity.size] * panel_size / 2)

        # Map the entity's color
        color_map = {
            Colors.RED: (0, 0, 255),      # BGR format
            Colors.BLUE: (255, 0, 0),
            Colors.GREEN: (0, 255, 0),
            Colors.YELLOW: (0, 255, 255),
            Colors.PURPLE: (255, 0, 255),
        }

        color = color_map[entity.color]
        angle = angle_map[entity.angle] * pi / 180  # Convert to radians

        # Determine the correct rendering function based on the shape
        if isinstance(entity, Line):
            # Render the line
            shape_renderers.get(entity.linetype)(img, center, size, color, entity.linewidth)
        elif isinstance(entity, BigShape):
            # Render the BigShape (such as triangle, square, etc.)
            shape_renderers.get(entity.shape)(img, center, size, color, angle)
    
    return img

# Shape Rendering Functions

def render_triangle(img, center, size, color, angle):
    scale_factor = 1.7  # Scale the size up slightly for better proportion
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2  # Half the base length
    height = adjusted_size * np.sqrt(3) / 2  # Height of an equilateral triangle

    # Define the vertices relative to the center
    pts = np.array([ 
       [center[0], center[1] - 2 * height / 3],  # Top vertex
       [center[0] - half_size, center[1] + height / 3],  # Bottom-left vertex
       [center[0] + half_size, center[1] + height / 3],  # Bottom-right vertex
    ], np.float32)

    # Apply rotation using OpenCV's transformation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    pts = cv2.transform(np.array([pts]), rotation_matrix)[0].astype(np.int32)

    # Draw the triangle
    cv2.fillPoly(img, [pts], color)

def render_square(img, center, size, color, angle):
    half_size = size / 2
    pts = np.array([
        [center[0] - half_size, center[1] - half_size],
        [center[0] + half_size, center[1] - half_size],
        [center[0] + half_size, center[1] + half_size],
        [center[0] - half_size, center[1] + half_size],
    ], np.float32)
    
    # Apply rotation
    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    pts = cv2.transform(np.array([pts]), rotation_matrix)[0].astype(np.int32)

    # Draw the square
    cv2.fillPoly(img, [pts], color)

def render_pentagon(img, center, size, color, angle):
    pts = []
    for i in range(5):
        x = center[0] + size * cos(2 * pi * i / 5 + angle)
        y = center[1] + size * sin(2 * pi * i / 5 + angle)
        pts.append((int(x), int(y)))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color)

def render_hexagon(img, center, size, color, angle):
    pts = []
    for i in range(6):
        x = center[0] + size * cos(2 * pi * i / 6 + angle)
        y = center[1] + size * sin(2 * pi * i / 6 + angle)
        pts.append((int(x), int(y)))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color)

def render_decagon(img, center, size, color, angle):
    pts = []
    for i in range(10):
        x = center[0] + size * cos(2 * pi * i / 10 + angle)
        y = center[1] + size * sin(2 * pi * i / 10 + angle)
        pts.append((int(x), int(y)))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color)

def render_circle(img, center, size, color, angle):
    cv2.circle(img, center, int(size), color, -1)



# Line rendering functions

# Line rendering functions

def render_solid_line(img, center, size, linewidth):
    # Use LineColors.BLACK for color
    color = (0, 0, 0)  # Black in BGR format
    
    # Map the line width using the linewidth_map
    thickness = linewidth_map.get(linewidth, 1)  # Default to 1 if not found
    
    line_start = (center[0] - size // 2, center[1] - size // 2)
    line_end = (center[0] + size // 2, center[1] + size // 2)
    
    cv2.line(img, line_start, line_end, color, thickness)

def render_dashed_line(img, center, size, linewidth):
    # Use LineColors.BLACK for color
    color = (0, 0, 0)  # Black in BGR format
    
    thickness = linewidth_map.get(linewidth, 1)  # Map the linewidth to an integer
    
    # Dash pattern settings
    dash_length = size // 10  # Length of each dash segment
    gap_length = size // 20   # Gap between dashes
    
    # Calculate the direction of the line
    line_start = (center[0] - size // 2, center[1] - size // 2)
    line_end = (center[0] + size // 2, center[1] + size // 2)
    
    direction = np.array(line_end) - np.array(line_start)
    direction = direction / np.linalg.norm(direction)  # Normalize the direction

    # Draw dashes along the line
    current_position = np.array(line_start)
    while np.linalg.norm(current_position - np.array(line_end)) > dash_length:
        dash_end = current_position + direction * dash_length
        cv2.line(img, tuple(current_position.astype(int)), tuple(dash_end.astype(int)), color, thickness)
        current_position = dash_end + direction * gap_length

def render_dotted_line(img, center, size, linewidth):
    # Use LineColors.BLACK for color
    color = (0, 0, 0)  # Black in BGR format
    
    thickness = linewidth_map.get(linewidth, 1)  # Map the linewidth to an integer
    
    # Dot pattern settings
    dot_radius = size // 20  # Radius of each dot
    gap_length = size // 10   # Gap between dots
    
    # Calculate the direction of the line
    line_start = (center[0] - size // 2, center[1] - size // 2)
    line_end = (center[0] + size // 2, center[1] + size // 2)
    
    direction = np.array(line_end) - np.array(line_start)
    direction = direction / np.linalg.norm(direction)  # Normalize the direction

    # Draw dots along the line
    current_position = np.array(line_start)
    while np.linalg.norm(current_position - np.array(line_end)) > dot_radius:
        cv2.circle(img, tuple(current_position.astype(int)), dot_radius, color, thickness)
        current_position = current_position + direction * (dot_radius * 2 + gap_length)

