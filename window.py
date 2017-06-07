from gi.repository import Gdk

def position(window, config):
    window.unmaximize()
    window.set_shadow_width(0,0,0,0)

    offx, offy = offsets(window)
    window.move_resize(
        config['x1'],
        config['y1'],
        config['w'] - (offx * 2),
        config['h'] - (offx + offy)
    )

def active_window():
    screen = Gdk.Screen.get_default()
    window = screen.get_active_window()

    if no_window(screen, window):
        return None

    return window


def offsets(window):
    origin = window.get_origin()
    root = window.get_root_origin()
    return (origin.x - root.x, origin.y - root.y)


def no_window(screen, window):
    return (
        not screen.supports_net_wm_hint(
            Gdk.atom_intern('_NET_ACTIVE_WINDOW', True)
        ) or
        not screen.supports_net_wm_hint(
            Gdk.atom_intern('_NET_WM_WINDOW_TYPE', True)
        ) or
        window.get_type_hint().value_name == 'GDK_WINDOW_TYPE_HINT_DESKTOP'
    )
