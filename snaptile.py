#!/usr/bin/env python3

from __future__ import print_function

import signal
from Xlib import display, X

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from window import position
from keyutil import get_posmap, initkeys

keymap = [
    ['Q', 'W', 'E', 'R'],
    ['A', 'S', 'D', 'F'],
    ['Z', 'X', 'C', 'V']
]

def global_inital_states():
    displ = display.Display()
    rt = displ.screen().root
    rt.change_attributes(event_mask=X.KeyPressMask)

    return (
        displ,
        rt,
        {
            'code': 0,
            'pressed': False
        },
        get_posmap(keymap, displ)
    )

disp, root, lastkey_state, posmap = global_inital_states()


def run():
    initkeys(keymap, disp, root)
    for _ in range(0, root.display.pending_events()):
        root.display.next_event()
    GObject.io_add_watch(root.display, GObject.IO_IN, checkevt)
    print('Snaptile running. Press CTRL+C to quit.')
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()

def checkevt(_, __, handle=None):
    global lastkey_state

    handle = handle or root.display
    for _ in range(0, handle.pending_events()):
        event = handle.next_event()

        if event.type == X.KeyPress:

            if event.detail not in posmap:
                break

            if not lastkey_state['pressed']:
                handleevt(event.detail, event.detail)

            else:
                handleevt(lastkey_state['code'], event.detail)

            lastkey_state = {
                'code': event.detail,
                'pressed': True
            }

        if event.type == X.KeyRelease:
            if event.detail == lastkey_state['code']:
                lastkey_state['pressed'] = False

    return True

def handleevt(startkey, endkey):
    position(
        posmap[startkey],
        posmap[endkey]
    )

if __name__ == '__main__':
    run()
