#!/usr/bin/env python3

from __future__ import print_function

import sys, getopt

import signal
from Xlib import display, X

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from window import position
from keyutil import get_posmap, initkeys

keymaps = {
    "qwerty":
    (['Q', 'W', 'E', 'R'],
     ['A', 'S', 'D', 'F'],
     ['Z', 'X', 'C', 'V']),
    "azerty":
    (['A', 'Z', 'E', 'R'],
     ['Q', 'S', 'D', 'F'],
     ['W', 'X', 'C', 'V']),
    "qwertz":
    (['Q', 'W', 'E', 'R'],
     ['A', 'S', 'D', 'F'],
     ['Y', 'X', 'C', 'V']),
    "colemak":
    (['Q', 'W', 'F', 'P'],
     ['A', 'R', 'S', 'T'],
     ['Z', 'X', 'C', 'V']),
    "dvorak":
    (['apostrophe', 'comma', 'period', 'P'],
     ['A', 'O', 'E', 'U'],
     ['semicolon', 'Q', 'J', 'K']),
}

dualMonitorKeymaps = {
    "qwerty":
    (['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I'],
     ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'],
     ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'comma']),
    "azerty":
    (['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I'],
     ['Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K'],
     ['W', 'X', 'C', 'V', 'B', 'N', 'comma', 'semicolon']),
    "qwertz":
    (['Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I'],
     ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'],
     ['Y', 'X', 'C', 'V', 'B', 'N', 'M', 'comma']),
    "colemak":
    (['Q', 'W', 'F', 'P', 'G', 'J', 'L', 'U'],
     ['A', 'R', 'S', 'T', 'D', 'H', 'N', 'E'],
     ['Z', 'X', 'C', 'V', 'B', 'K', 'M', 'comma']),
    "dvorak":
    (['apostrophe', 'comma', 'period', 'P', 'Y', 'F', 'G', 'C'],
     ['A', 'O', 'E', 'U', 'I', 'D', 'H', 'T'],
     ['semicolon', 'Q', 'J', 'K', 'X', 'B', 'M', 'W']),
}



def autodetectKeyboard():
    try:
        import sdl2
        import sdl2.keyboard
        from sdl2 import keycode
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        keys = bytes(sdl2.keyboard.SDL_GetKeyFromScancode(sc) for sc in (keycode.SDL_SCANCODE_Q, keycode.SDL_SCANCODE_W, keycode.SDL_SCANCODE_Y))
        keyMap = {
            b'qwy': 'qwerty',
            b'azy': 'azerty',
            b'qwz': 'qwertz',
            b'qwj': 'colemak',
            b'\',f': 'dvorak',
        }
        if keys in keyMap:
            return keyMap.get(keys, 'unknown')
    except:
        print("Could not detect keyboard (is PySDL2 installed?). Falling back to qwerty.")
        return "qwerty"


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

global disp, root, lastkey_state, posmap;


def run():
    mask = None

    opts, args = getopt.getopt(sys.argv[1:], "hdWk:")
    keyboardLayout = autodetectKeyboard()
    isDualMonitor = False
    
    for opt in opts:
        if opt[0] == '-h':
            print ('Snaptile.py')
            print ('-d expanded dual-monitor keybinds')
            print ('-W use Windows key')
            print ('-h this help text')
            print ('-k <keymap> to specify a keyboard layout (eg. qwerty)')
            sys.exit()
        elif opt[0] == '-d':
            isDualMonitor = True
        elif opt[0] == '-W':
            mask = 'Windows'
        elif opt[0] == '-k':
            keyboardLayout = opt[1]

    global keymap;
    keymapSource = keymaps
    if isDualMonitor:
        keymapSource = dualMonitorKeymaps
    if keyboardLayout in keymapSource:
        keymap = keymapSource[keyboardLayout]
    else:
        print("Unsupported keyboard layout. Falling back to qwerty.")
        keymap = keymapSource["qwerty"]

    global disp, root, lastkey_state, posmap
    disp, root, lastkey_state, posmap = global_inital_states()

    initkeys(keymap, disp, root, mask)
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
