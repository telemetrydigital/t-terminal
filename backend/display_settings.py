import os

def set_resolution(resolution):
    """
    Nastavenie rozlíšenia obrazovky.
    """
    width, height = resolution.split("x")
    os.system(f"xrandr --fb {width}x{height}")

def set_rotation(rotation):
    """
    Nastavenie rotácie obrazovky.
    """
    rotation_map = {
        "0°": "normal",
        "90°": "right",
        "180°": "inverted",
        "270°": "left"
    }
    os.system(f"xrandr --output HDMI-1 --rotate {rotation_map[rotation]}")

def toggle_cursor(hide):
    """
    Skrytie alebo zobrazenie kurzora.
    """
    if hide:
        os.system("xsetroot -cursor empty_cursor empty_cursor")
    else:
        os.system("xsetroot -cursor_name left_ptr")

