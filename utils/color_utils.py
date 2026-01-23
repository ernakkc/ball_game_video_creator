def to_rgba_float(color):
    """Normalize a color to an RGBA tuple with floats in 0..1.

    Accepts:
    - (r,g,b) ints 0..255
    - (r,g,b,a) ints 0..255 or floats 0..1
    - (r,g,b) floats 0..1

    Returns (r,g,b,a) with floats in 0..1.
    """
    if color is None:
        return None

    # already floats 0..1
    try:
        if all(isinstance(c, float) and 0.0 <= c <= 1.0 for c in color):
            if len(color) == 3:
                return (color[0], color[1], color[2], 1.0)
            if len(color) == 4:
                return tuple(color)
    except Exception:
        pass

    # ints 0..255
    try:
        if all(isinstance(c, int) for c in color):
            if len(color) == 3:
                r, g, b = color
                return (r / 255.0, g / 255.0, b / 255.0, 1.0)
            if len(color) == 4:
                r, g, b, a = color
                a = a / 255.0 if a > 1 else a
                return (r / 255.0, g / 255.0, b / 255.0, a)
    except Exception:
        pass

    # mixed or unexpected — attempt safe conversion
    try:
        comps = [float(c) for c in color]
        if len(comps) == 3:
            r, g, b = comps
            if max(comps) > 1.0:
                return (r / 255.0, g / 255.0, b / 255.0, 1.0)
            return (r, g, b, 1.0)
        if len(comps) == 4:
            r, g, b, a = comps
            if max(comps) > 1.0:
                a = a / 255.0 if a > 1 else a
                return (r / 255.0, g / 255.0, b / 255.0, a)
            return (r, g, b, a)
    except Exception:
        pass

    # fallback
    return (0.5, 0.5, 0.5, 1.0)
