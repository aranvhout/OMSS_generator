import cv2
import numpy as np
from math import cos, sin, pi
from entity import Shapes, Sizes, Colors, Angles, Positions, Linetypes, Linelengths, Linewidths, Line, BigShape, LittleShape

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
        Colors.RED: (0, 0, 255),      # BGR format
        Colors.BLUE: (255, 0, 0),
        Colors.GREEN: (0, 255, 0),
        Colors.YELLOW: (0, 255, 255),
        Colors.PURPLE: (255, 0, 255),
    }
    
    
LINEWIDTH_MAP = {
        Linewidths.THIN: 3,
        Linewidths.MEDIUM: 5,
        Linewidths.THICK: 7
    }



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
        Shapes.HEXAGON: render_hexagon,
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

    


# Updated Shape Rendering Functions
def render_triangle(img, center, size, entity):
    color = COLOR_MAP[entity.color]
    angle = ANGLE_MAP[entity.angle] * pi / 180
    scale_factor = 1.7
    adjusted_size = size * scale_factor
    half_size = adjusted_size / 2
    height = adjusted_size * np.sqrt(3) / 2

    pts = np.array([
        [center[0], center[1] - 2 * height / 3],
        [center[0] - half_size, center[1] + height / 3],
        [center[0] + half_size, center[1] + height / 3],
    ], np.float32)

    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    pts = cv2.transform(np.array([pts]), rotation_matrix)[0].astype(np.int32)
    cv2.fillPoly(img, [pts], color)


def render_square(img, center, size, entity):
    color = COLOR_MAP[entity.color]
    angle = ANGLE_MAP[entity.angle] * pi / 180
    scale_factor = 1.3
    size = size * scale_factor
    half_size = size / 2

    pts = np.array([
        [center[0] - half_size, center[1] - half_size],
        [center[0] + half_size, center[1] - half_size],
        [center[0] + half_size, center[1] + half_size],
        [center[0] - half_size, center[1] + half_size],
    ], np.float32)

    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    pts = cv2.transform(np.array([pts]), rotation_matrix)[0].astype(np.int32)
    cv2.fillPoly(img, [pts], color)


def render_pentagon(img, center, size, entity):
    color = COLOR_MAP[entity.color]
    angle = ANGLE_MAP[entity.angle] * pi / 180
    pts = []
    for i in range(5):
        x = center[0] + size * cos(2 * pi * i / 5 + angle)
        y = center[1] + size * sin(2 * pi * i / 5 + angle)
        pts.append((int(x), int(y)))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color)


def render_hexagon(img, center, size, entity):
    color = COLOR_MAP[entity.color]
    angle = ANGLE_MAP[entity.angle] * pi / 180
    pts = []
    for i in range(6):
        x = center[0] + size * cos(2 * pi * i / 6 + angle)
        y = center[1] + size * sin(2 * pi * i / 6 + angle)
        pts.append((int(x), int(y)))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color)


def render_decagon(img, center, size, entity):
    color = COLOR_MAP[entity.color]
    angle = ANGLE_MAP[entity.angle] * pi / 180
    pts = []
    for i in range(10):
        x = center[0] + size * cos(2 * pi * i / 10 + angle)
        y = center[1] + size * sin(2 * pi * i / 10 + angle)
        pts.append((int(x), int(y)))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], color)


def render_circle(img, center, length, entity):
    color = COLOR_MAP[entity.color]
    cv2.circle(img, center, int(length), color, -1)


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
    Renders a solid line with rotation based on entity.angle.
    """
    color = (0, 0, 0)  # Default black color
    thickness = LINEWIDTH_MAP.get(entity.linewidth, 1)
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert to radians
    
    # Calculate unrotated start and end points
    line_start = (center[0] - length // 2, center[1])
    line_end = (center[0] + length // 2, center[1])
    
    # Rotate points around the center
    line_start = rotate_point(line_start, center, angle)
    line_end = rotate_point(line_end, center, angle)
    
    # Draw the rotated line
    cv2.line(img, line_start, line_end, color, thickness)

def render_dashed_line(img, center, length, entity, gap_multiplier=1):
    """
    Renders a dashed line with rotation based on entity.angle.
    """
    color = (0, 0, 0)  # Default black color
    thickness = LINEWIDTH_MAP.get(entity.linewidth, 1)
    angle = ANGLE_MAP[entity.angle] * pi / 180  # Convert to radians
    dash_length = length // 10
    gap_length = dash_length * gap_multiplier
    total_length = length
    line_start_x = center[0] - total_length // 2
    line_end_x = center[0] + total_length // 2

    # Generate dashes
    dashes = []
    for start_x in range(line_start_x, line_end_x, dash_length + gap_length):
        dash_end_x = min(start_x + dash_length, line_end_x)  # Ensure it doesn't overshoot
        dash_start = (start_x, center[1])
        dash_end = (dash_end_x, center[1])
        dashes.append((dash_start, dash_end))
    
    # Rotate and draw each dash
    for dash_start, dash_end in dashes:
        dash_start = rotate_point(dash_start, center, angle)
        dash_end = rotate_point(dash_end, center, angle)
        cv2.line(img, dash_start, dash_end, color, thickness)

def render_large_dashed_line(img, center, length, entity):
    """
    Renders a dashed line with larger gaps and rotation based on entity.angle.
    """
    render_dashed_line(img, center, length, entity, gap_multiplier=3)


