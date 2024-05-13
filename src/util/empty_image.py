from pyglet.image import ImageData

_black_color = 0x00_00_00
_magenta_color = 0xff_00_ff

def _get_pattern_data(width, height):
    data_pixels = []
    for x in range(width):
        for y in range(height):
            if x < (width // 2) != y < (height // 2):
                data_pixels.append()
            else:
                data_pixels.append(b'')

empty_image_width = 16
empty_image_height = 16
empty_image_data = b''.join(
    [  ]
)

empty_image = ImageData()