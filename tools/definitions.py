from dataclasses import dataclass

@dataclass
class ToolDefinition:
    """
    Defines the properties of a single tool in the image editor.

    Attributes:
        name (str): The display name of the tool (e.g., "Pen", "Eraser").
        icon (str): The file path to the SVG icon representing the tool.
        tool_id (int): A unique integer identifier for the tool.
        shortcut (str): An optional keyboard shortcut for activating the tool. Defaults to an empty string.
        description (str): A brief description of the tool's function. Defaults to an empty string.
        finished (bool): A flag indicating whether the tool's implementation is considered complete. Defaults to False.
    """
    name: str
    icon: str
    tool_id: int
    shortcut: str = ""
    description: str = ""
    finished: bool = False

TOOL_PEN = ToolDefinition("Pen", "svgicons/pen-gray.svg", 1000, "P", "Pen Tool", True)
'''
Represents the Pen tool.
- `name`: "Pen" - Display name.
- `icon`: "svgicons/pen-gray.svg" - Path to icon.
- `tool_id`: 1000 - Unique ID.
- `shortcut`: "P" - Keyboard shortcut.
- `description`: "Pen Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_BRUSH = ToolDefinition("Brush", "svgicons/brush.svg", 1001, "B", "Brush Tool", False)
'''
Represents the Brush tool.
- `name`: "Brush" - Display name.
- `icon`: "svgicons/brush.svg" - Path to icon.
- `tool_id`: 1001 - Unique ID.
- `shortcut`: "B" - Keyboard shortcut.
- `description`: "Brush Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_LINE = ToolDefinition("Line", "svgicons/line-gray.svg", 1002, "L", "Line Tool", True)
'''
Represents the Line tool.
- `name`: "Line" - Display name.
- `icon`: "svgicons/line-gray.svg" - Path to icon.
- `tool_id`: 1002 - Unique ID.
- `shortcut`: "L" - Keyboard shortcut.
- `description`: "Line Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_RECT = ToolDefinition("Rectangle", "svgicons/rectangle.svg", 1003, "R", "Rectangle Tool", True)
'''
Represents the Rectangle tool.
- `name`: "Rectangle" - Display name.
- `icon`: "svgicons/rectangle.svg" - Path to icon.
- `tool_id`: 1003 - Unique ID.
- `shortcut`: "R" - Keyboard shortcut.
- `description`: "Rectangle Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_CIRCLE = ToolDefinition("Circle", "svgicons/circle-gray.svg", 1004, "C", "Circle Tool", True)
'''
Represents the Circle tool.
- `name`: "Circle" - Display name.
- `icon`: "svgicons/circle-gray.svg" - Path to icon.
- `tool_id`: 1004 - Unique ID.
- `shortcut`: "C" - Keyboard shortcut.
- `description`: "Circle Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_SPRAY = ToolDefinition("Spray", "svgicons/spray-gray.svg", 1005, "S", "Spray Tool", True)
'''
Represents the Spray tool.
- `name`: "Spray" - Display name.
- `icon`: "svgicons/spray-gray.svg" - Path to icon.
- `tool_id`: 1005 - Unique ID.
- `shortcut`: "S" - Keyboard shortcut.
- `description`: "Spray Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_FILL = ToolDefinition("Fill", "svgicons/fill.svg", 1006, "F", "Fill Tool", True)
'''
Represents the Fill tool.
- `name`: "Fill" - Display name.
- `icon`: "svgicons/fill.svg" - Path to icon.
- `tool_id`: 1006 - Unique ID.
- `shortcut`: "F" - Keyboard shortcut.
- `description`: "Fill Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_TEXT = ToolDefinition("Text", "svgicons/text.svg", 1007, "T", "Text Tool", False)
'''
Represents the Text tool.
- `name`: "Text" - Display name.
- `icon`: "svgicons/text.svg" - Path to icon.
- `tool_id`: 1007 - Unique ID.
- `shortcut`: "T" - Keyboard shortcut.
- `description`: "Text Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_ERASER = ToolDefinition("Eraser", "svgicons/eraser-gray.svg", 1008, "E", "Eraser Tool", False)
'''
Represents the Eraser tool.
- `name`: "Eraser" - Display name.
- `icon`: "svgicons/eraser-gray.svg" - Path to icon.
- `tool_id`: 1008 - Unique ID.
- `shortcut`: "E" - Keyboard shortcut.
- `description`: "Eraser Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_PAN = ToolDefinition("Pan", "svgicons/pan-gray.svg", 1010, "P", "Pan Tool", False)
'''
Represents the Pan tool.
- `name`: "Pan" - Display name.
- `icon`: "svgicons/pan-gray.svg" - Path to icon.
- `tool_id`: 1010 - Unique ID.
- `shortcut`: "P" - Keyboard shortcut.
- `description`: "Pan Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_DROPPER = ToolDefinition("Dropper", "svgicons/dropper.svg", 1011, "D", "Dropper Tool", True)
'''
Represents the Dropper (color picker) tool.
- `name`: "Dropper" - Display name.
- `icon`: "svgicons/dropper.svg" - Path to icon.
- `tool_id`: 1011 - Unique ID.
- `shortcut`: "D" - Keyboard shortcut.
- `description`: "Dropper Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_ROUNDED_RECT = ToolDefinition("Rounded Rectangle", "svgicons/rounded-rectangle.svg", 1012, "O", "Rounded Rectangle Tool", True)
'''
Represents the Rounded Rectangle tool.
- `name`: "Rounded Rectangle" - Display name.
- `icon`: "svgicons/rounded-rectangle.svg" - Path to icon.
- `tool_id`: 1012 - Unique ID.
- `shortcut`: "O" - Keyboard shortcut.
- `description`: "Rounded Rectangle Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_ELLIPSE = ToolDefinition("Ellipse", "svgicons/ellipse-gray.svg", 1013, "L", "Ellipse Tool", True)
'''
Represents the Ellipse tool.
- `name`: "Ellipse" - Display name.
- `icon`: "svgicons/ellipse-gray.svg" - Path to icon.
- `tool_id`: 1013 - Unique ID.
- `shortcut`: "L" - Keyboard shortcut.
- `description`: "Ellipse Tool" - Function description.
- `finished`: True - Implementation complete.
'''
TOOL_WAND = ToolDefinition("Wand", "svgicons/wand.svg", 1014, "W", "Wand Tool", False)
'''
Represents the Magic Wand selection tool.
- `name`: "Wand" - Display name.
- `icon`: "svgicons/wand.svg" - Path to icon.
- `tool_id`: 1014 - Unique ID.
- `shortcut`: "W" - Keyboard shortcut.
- `description`: "Wand Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_POLYGON = ToolDefinition("Polygon", "svgicons/polygon-gray.svg", 1015, "G", "Polygon Tool", False)
'''
Represents the Polygon tool.
- `name`: "Polygon" - Display name.
- `icon`: "svgicons/polygon-gray.svg" - Path to icon.
- `tool_id`: 1015 - Unique ID.
- `shortcut`: "G" - Keyboard shortcut.
- `description`: "Polygon Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_BEZIER = ToolDefinition("Bezier", "svgicons/bezier-gray.svg", 1016, "B", "Bezier Tool", False)
'''
Represents the Bezier curve tool.
- `name`: "Bezier" - Display name.
- `icon`: "svgicons/bezier-gray.svg" - Path to icon.
- `tool_id`: 1016 - Unique ID.
- `shortcut`: "B" - Keyboard shortcut.
- `description`: "Bezier Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_SELECT_RECT = ToolDefinition("Select Rectangle", "svgicons/select-rectangle-gray.svg", 1017, "S", "Select Rectangle Tool", False)
'''
Represents the Rectangle Selection tool.
- `name`: "Select Rectangle" - Display name.
- `icon`: "svgicons/select-rectangle-gray.svg" - Path to icon.
- `tool_id`: 1017 - Unique ID.
- `shortcut`: "S" - Keyboard shortcut.
- `description`: "Select Rectangle Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_SELECT_CIRCLE = ToolDefinition("Select Circle", "svgicons/select-circle-gray.svg", 1018, "S", "Select Circle Tool", False)
'''
Represents the Circle Selection tool.
- `name`: "Select Circle" - Display name.
- `icon`: "svgicons/select-circle-gray.svg" - Path to icon.
- `tool_id`: 1018 - Unique ID.
- `shortcut`: "S" - Keyboard shortcut.
- `description`: "Select Circle Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_SELECT_POLYGON = ToolDefinition("Select Polygon", "svgicons/select-polygon.svg", 1019, "S", "Select Polygon Tool", False)
'''
Represents the Polygon Selection tool.
- `name`: "Select Polygon" - Display name.
- `icon`: "svgicons/select-polygon.svg" - Path to icon.
- `tool_id`: 1019 - Unique ID.
- `shortcut`: "S" - Keyboard shortcut.
- `description`: "Select Polygon Tool" - Function description.
- `finished`: False - Implementation not complete.
'''
TOOL_SELECT_LASSO = ToolDefinition("Select Lasso", "svgicons/lasso_select.svg", 1020, "S", "Select Lasso Tool", False)
TOOL_SELECT_PATH = ToolDefinition("Select Path", "svgicons/select-path.svg", 1021, "S", "Select Path Tool", False)
TOOL_CROP = ToolDefinition("Crop", "svgicons/crop.svg", 1022, "C", "Crop Tool", False)

ALL_TOOLS = [
    TOOL_PEN,
    TOOL_BRUSH,
    TOOL_LINE,
    TOOL_RECT,
    TOOL_CIRCLE,
    TOOL_SPRAY,
    TOOL_FILL,
    TOOL_TEXT,
    TOOL_ERASER,
    TOOL_PAN,
    TOOL_DROPPER,
    TOOL_ROUNDED_RECT,
    TOOL_ELLIPSE,
    TOOL_WAND,
    TOOL_POLYGON,
    TOOL_BEZIER,
    TOOL_SELECT_RECT,
    TOOL_SELECT_CIRCLE,
    TOOL_SELECT_POLYGON,
    TOOL_SELECT_LASSO,
    TOOL_SELECT_PATH,
    TOOL_CROP
]
