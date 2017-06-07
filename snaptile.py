import signal
from Xlib import display, X

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject  # noqa
from window import position
from keyutil import get_posmap, initkeys

def get_globals():
    displ = display.Display()
    rt = displ.screen().root
    rt.change_attributes(event_mask=X.KeyPressMask)
    return (displ, rt)

disp, root = get_globals()

lastkey = 0
lastpressed = False
keymap = [
    ['Q', 'W', 'E', 'R'],
    ['A', 'S', 'D', 'F'],
    ['Z', 'X', 'C', 'V']
]

posmap = get_posmap(keymap, disp)

def run():
    initkeys(keymap, disp, root)
    for event in range(0, root.display.pending_events()):
        root.display.next_event()
    GObject.io_add_watch(root.display, GObject.IO_IN, checkevt)
    print('Snaptile running. Press CTRL+C to cancel.')
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()

def checkevt(source, condition, handle=None):
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

if __name__ == '__main__':
    run()
