from Xlib.keysymdef import latin1
from functools import reduce
from Xlib import X

def get_posmap(keymap, disp):

    posmap = {}
    for i, row in enumerate(keymap):
        for j, key in enumerate(row):
            posmap[keycode(key, disp)] = (i, j)

    return posmap

def initkeys(keymap, disp, root):

    return [
        initkey(
            keycode(key, disp),
            root
        ) for key in reduce(lambda x, y: x + y, keymap)
    ]

def initkey(code, root):

    root.grab_key(
        code,
        X.ControlMask | X.Mod1Mask,
        1,
        X.GrabModeAsync,
        X.GrabModeAsync
    )

    root.grab_key(
        code,
        X.ControlMask | X.Mod1Mask | X.Mod2Mask,
        1,
        X.GrabModeAsync,
        X.GrabModeAsync
    )

    return code

def keycode(key, disp):
    return disp.keysym_to_keycode(
        getattr(
            latin1,
            'XK_{}'.format(key)
        )
    )
