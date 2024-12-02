import cv2
import numpy as np
from math import cos, sin, pi
from entity import Shapes, Sizes, Colors, Angles

def render_entity(entity, panel_size=500, background_color=(255, 255, 255)): #white background
    """
    Render an entity on a square canvas and return the image.
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

    # Determine the center and size
    center = (panel_size // 2, panel_size // 2)
    size_factor = {
        Sizes.SMALL: 0.3,
        Sizes.MEDIUM: 0.5,
        Sizes.LARGE: 0.9
    }
    color_map = {
        Colors.RED: (0, 0, 255),      # BGR format
        Colors.BLUE: (255, 0, 0),
        Colors.GREEN: (0, 255, 0),
        Colors.YELLOW: (0, 255, 255),
        Colors.PURPLE: (255, 0, 255),
    }

    # Calculate size and color
    size = int(size_factor[entity.size] * panel_size / 2)
    color = color_map[entity.color]
    angle = angle_map[entity.angle] * pi / 180  # Convert to radians

    # Draw the shape
    if entity.shape == Shapes.TRIANGLE:
        # Adjust size to make the triangle larger
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
        rotation_matrix = cv2.getRotationMatrix2D(center, -angle_map[entity.angle], 1.0)
        pts = cv2.transform(np.array([pts]), rotation_matrix)[0].astype(np.int32)
    
        # Draw the triangle
        cv2.fillPoly(img, [pts], color)

    elif entity.shape == Shapes.SQUARE:
        # Apply scaling factor directly to the calculated size of the square's vertices
        scale_factor = 1.5  # Scale factor for the square
        half_size = size / 2  # Half the original side length

        # Scale the half_size to adjust the square's vertices
        scaled_half_size = half_size * scale_factor

        # Calculate the vertices of the square using the scaled half size
        pts = np.array([
            [center[0] - scaled_half_size, center[1] - scaled_half_size],  # Top-left
            [center[0] + scaled_half_size, center[1] - scaled_half_size],  # Top-right
            [center[0] + scaled_half_size, center[1] + scaled_half_size],  # Bottom-right
            [center[0] - scaled_half_size, center[1] + scaled_half_size],  # Bottom-left
            ], np.float32)

        # Apply rotation using OpenCV's transformation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, -angle_map[entity.angle], 1.0)
        pts = cv2.transform(np.array([pts]), rotation_matrix)[0].astype(np.int32)

        # Draw the rotated square
        cv2.fillPoly(img, [pts], color)

    


    elif entity.shape == Shapes.PENTAGON:
        pts = []
        for i in range(5):
            x = center[0] + size * cos(2 * pi * i / 5 + angle)
            y = center[1] + size * sin(2 * pi * i / 5 + angle)
            pts.append((int(x), int(y)))
        pts = np.array(pts, np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(img, [pts], color)
    elif entity.shape == Shapes.HEXAGON:
        pts = []
        for i in range(6):
            x = center[0] + size * cos(2 * pi * i / 6 + angle)
            y = center[1] + size * sin(2 * pi * i / 6 + angle)
            pts.append((int(x), int(y)))
        pts = np.array(pts, np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(img, [pts], color)
    elif entity.shape == Shapes.CIRCLE:
        cv2.circle(img, center, int(size), color, -1)
    elif entity.shape == Shapes.DECAGON:
        pts = []
        for i in range(10):  # 10 sides for a decagon
            x = center[0] + size * cos(2 * pi * i / 10 + angle)
            y = center[1] + size * sin(2 * pi * i / 10 + angle)
            pts.append((int(x), int(y)))
        pts = np.array(pts, np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(img, [pts], color)

    return img


def render_matrix(entities, row_lengths, panel_size=1500, background_color=(255, 255, 255), line_color=(0, 0, 0), line_thickness=5):
    """
    Render a grid of entities with lines between the cells and return the composite image, where each row can have a different number of columns.
    
    Args:
        entities: A 2D list of entities (list of lists) corresponding to the grid.
        row_lengths: A list of tuples, each representing the range of columns for that row (e.g. [(0, 3), (0, 2), (0, 3)]).
        panel_size: Size of the entire grid panel in pixels (square).
        background_color: Background color as an RGB tuple.
        line_color: Color of the lines between cells in BGR format.
        line_thickness: Thickness of the grid lines.
    
    Returns:
        Composite grid image with lines as a NumPy array.
    """
    rows = len(row_lengths)  # Number of rows
    cols = max(end - start for start, end in row_lengths)  # Maximum number of columns in any row
    cell_size = panel_size // max(rows, cols)  # Size of each grid cell
    
    # Create a blank canvas with background color
    img = np.ones((panel_size, panel_size, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)
    
    # Draw the grid and render the entities
    for r, (start_col, end_col) in enumerate(row_lengths):
        for c in range(start_col, end_col):
            entity = entities[r][c] if r < len(entities) and c < len(entities[r]) else None
            # Render the entity
            entity_img = render_entity(entity, panel_size=cell_size, background_color=background_color) if entity is not None else np.ones((cell_size, cell_size, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)
            
            # Calculate the top-left corner of the current grid cell
            y_start, x_start = r * cell_size, c * cell_size
            
            # Place the rendered entity into the composite image
            img[y_start:y_start + cell_size, x_start:x_start + cell_size] = entity_img
    
    # Draw vertical lines
    for r in range(1, rows):
        y = r * cell_size
        cv2.line(img, (0, y), (panel_size, y), line_color, line_thickness)
    
    # Draw horizontal lines
    for c in range(1, cols):
        x = c * cell_size
        cv2.line(img, (x, 0), (x, panel_size), line_color, line_thickness)

    return img






