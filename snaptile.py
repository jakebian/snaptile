import signal
from Xlib import display, X
from Xlib.keysymdef import latin1

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject  # noqa
from window import position, active_window

display = display.Display()
root = display.screen().root
root.change_attributes(event_mask=X.KeyPressMask)

def initkeys():
    initkey(latin1.XK_A)

def initkey(keycode):
    root.grab_key(
        display.keysym_to_keycode(keycode),
        X.ControlMask | X.Mod1Mask,
        1,
        X.GrabModeAsync,
        X.GrabModeAsync
    )

    root.grab_key(
        display.keysym_to_keycode(keycode),
        X.ControlMask | X.Mod1Mask | X.Mod2Mask,
        1,
        X.GrabModeAsync,
        X.GrabModeAsync
    )

def _check_event(source, condition, handle=None):
    """ Check keyboard event has all the right buttons pressed. """
    handle = handle or root.display
    for _ in range(0, handle.pending_events()):
        event = handle.next_event()
        if event.type == X.KeyPress:
            _handle_event('lol')
    return True

def _handle_event(keypos):
    position(
        active_window(),
        {
            'x1': 0,
            'y1': 0,
            'w': 500,
            'h': 500
        }
    )
    print keypos


print('Snaptile running. Press CTRL+C to cancel.')

if __name__ == '__main__':
    initkeys()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    for event in range(0, root.display.pending_events()):
        root.display.next_event()
    GObject.io_add_watch(root.display, GObject.IO_IN, _check_event)
    Gtk.main()


