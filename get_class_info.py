# get_class_info.py
# Script to get the methods and bases of a class
# Usage:  python get_class_info.py <classname> [<string>]
# The parent classes will be listed, followed by the methods, filtered to just those containing <string>, if supplied (case-insensitive)
# Example output:
'''
    20:28: ~ ⦺ python get_class_info.py ArrowCircleTip BACKGROUND

    # Parent classes of ArrowCircleTip:

    ArrowTip
    VMobject
    Mobject
    object
    Circle
    Arc
    TipableVMobject

    # Methods of ArrowCircleTip containing 'BACKGROUND':

    add_background_rectangle()
    add_background_rectangle_to_family_members_with_points()
    add_background_rectangle_to_submobjects()
    color_using_background_image()
    get_background_image()
    match_background_image()
    set_background_stroke()

20:28: ~ ⦺ 
'''

import sys
from manim import *
from tint256 import *

def get_class_name(cls: object) -> str:
    return cls.__name__

def get_class_object(class_name: str) -> object:
    try:
        cls = getattr(sys.modules[__name__], class_name)
    except AttributeError:
        return None
    return cls

def get_methods(cls: object) -> list[str]:
    method_names = [a for a in dir(cls) if callable(getattr(cls, a)) and not a.startswith('__')]
    return method_names

def get_bases(cls: object) -> tuple[object]:
    classes = cls.__bases__
    return classes

def get_ancestors(cls: object) -> list[object]:
    ancestors = []
    bases = cls.__bases__
    if not bases:
        return []
    else:
        for base in bases:
            ancestors.append(base)
            ancestors += get_ancestors(base)
    return [*dict.fromkeys(ancestors)]  # Eliminate duplicates while preserving order

def get_descendants(cls: object) -> list[object]:
    descendants = []
    children = cls.__subclasses__()
    if not children:
        return []
    else:
        for subclass in children:
            descendants.append(subclass)
            descendants += get_descendants(subclass)
    return [*dict.fromkeys(descendants)]  # Eliminate duplicates while preserving order
    
def main():
    match(len(sys.argv)):
        case n if n < 2:
            return None
        case 2:
            grep_str = False
        case n if n > 2:
            grep_str = sys.argv[2]
    newline, parens = '\n', '()'
    quote = lambda s: f"'{s}'"
    cn = sys.argv[1]
    if (cls := get_class_object(cn)) is None:
        print(f'{newline}# The name {cn} is not a valid class name.{newline}- please check your spelling and try again!')
        sys.exit(0)

    # Show parent classes       
    print(tint256(f'{newline}Parent classes of {cn}:{newline}', 208, Style.UNDERLINED))
    for ancestor in get_ancestors(cls):
        print(tint256(get_class_name(ancestor), 85))

    # Show subclasses    
    print(tint256(f'{newline}Subclasses of {cn}:{newline}', 208, Style.UNDERLINED))
    for subclass in get_descendants(cls):
        print(tint256(get_class_name(subclass), 85))

    # Show methods
    if not 'nomethods' in sys.argv[2:]:
        print(tint256(f'{newline}Methods of {cn + ((" containing " + quote(grep_str)) if grep_str else "")}:{newline}', 208, Style.UNDERLINED))
        mm = get_methods(cls)
        column_width = max(len(s) for s in mm) + 6
        clr = 39
        for method_tuple in [mm[p:p+4] for p in range(0, len(mm), 4)]:
            line = ''
            for m in method_tuple:
                if not grep_str or grep_str and grep_str.lower() in m.lower():
                    line += (m + parens).ljust(column_width)
            print(tint256(line, clr := 266 - clr))
    

if __name__ == '__main__':
    main()
