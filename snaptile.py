import signal
from Xlib import display, X
from Xlib.keysymdef import latin1
from functools import reduce

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject  # noqa
from window import position

from Xlib.display import Display
from Xlib import X
from Xlib import protocol


display = display.Display()
root = display.screen().root
root.change_attributes(event_mask=X.KeyPressMask)

keymap = [
    ['Q', 'W', 'E', 'R'],
    ['A', 'S', 'D', 'F'],
    ['Z', 'X', 'C', 'V']
]

lastkey = 0
lastpressed = False

def keycode(key):
    return display.keysym_to_keycode(
        getattr(
            latin1,
            'XK_{}'.format(key)
        )
    )

def get_posmap(keymap):
    posmap = {}
    for i, row in enumerate(keymap):
        for j, key in enumerate(row):
            posmap[keycode(key)] = (i, j)
    return posmap


posmap = get_posmap(keymap)

def initkeys():
    return map(
        lambda key: initkey(
            keycode(key)
        ),
        reduce(lambda x, y: x + y, keymap)
    )


def initkey(keycode):
    root.grab_key(
        keycode,
        X.ControlMask | X.Mod1Mask,
        1,
        X.GrabModeAsync,
        X.GrabModeAsync
    )

    root.grab_key(
        keycode,
        X.ControlMask | X.Mod1Mask | X.Mod2Mask,
        1,
        X.GrabModeAsync,
        X.GrabModeAsync
    )
    return keycode

def checkevt(source, condition, handle=None):
    """ Check keyboard event has all the right buttons pressed. """
    handle = handle or root.display
    global lastkey
    global lastpressed
    for _ in range(0, handle.pending_events()):
        event = handle.next_event()
        if event.type == X.KeyPress:
            if not lastpressed:
                handleevt(event.detail, event.detail)
            else:
                handleevt(lastkey, event.detail)
            lastkey = event.detail
            lastpressed = True

        if event.type == X.KeyRelease:
            if event.detail == lastkey:
                lastpressed = False

    return True

def handleevt(startkey, endkey):
    position(
        posmap[startkey],
        posmap[endkey]
    )


print('Snaptile running. Press CTRL+C to cancel.')

if __name__ == '__main__':
    initkeys()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    for event in range(0, root.display.pending_events()):
        root.display.next_event()
    GObject.io_add_watch(root.display, GObject.IO_IN, checkevt)
    Gtk.main()


