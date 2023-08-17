from enum import IntEnum


class Style(IntEnum):
    NORMAL = 0
    BRIGHT = 1
    DIM = 2
    UNDERLINED = 4
    BACKGROUND = 7
    HIDDEN = 8
    STRIKEOUT = 9

def tint256(s, col, styles=Style.NORMAL):
    """
    Given a string and an ANSI escape code or a list of ANSI escape codes for style,
    append control characters appropriately to colour or add print effects to the string.
    """
    if not isinstance(styles, Style) and len(styles) == 1:
        styles = styles[0]
    if isinstance(styles, Style):
        return f'\u001B[{styles.value};38;5;{col}m{str(s)}\u001B[0m'
    ss = f'\u001B[{styles[0].value};38;5;{col}m{str(s)}\u001B[0m'
    return tint256(ss, col, styles[1:])
