# Type alias for color representation: (R, G, B, A) where each value is a float from 0 to 1
# Matches to System.Windows.Media.Color Sc{A,R,G,B} values
Color = tuple[float, float, float, float]

# Match the AP Suite random color cycle if no colors are defined
FALLBACK_COLOR_DEFINITIONS: list[Color] = [
    (0xff / 255, 0x00 / 255, 0x00 / 255, 0xff / 255),  # Red
    (0x00 / 255, 0x80 / 255, 0x00 / 255, 0xff / 255),  # Green
    (0x00 / 255, 0x00 / 255, 0xff / 255, 0xff / 255),  # Blue
    (0x00 / 255, 0xff / 255, 0xff / 255, 0xff / 255),  # Aqua
    (0x80 / 255, 0x00 / 255, 0x80 / 255, 0xff / 255),  # Purple
    (0xff / 255, 0xff / 255, 0x00 / 255, 0xff / 255),  # Yellow
    (0xff / 255, 0xc8 / 255, 0x00 / 255, 0xff / 255),
    (0xff / 255, 0xaf / 255, 0xaf / 255, 0xff / 255),
]