from gi.repository import Gdk

def position(startpos, endpos):
    window, screen = active_window()
    window.unmaximize()
    window.set_shadow_width(0, 0, 0, 0)
    workarea = screen.get_monitor_workarea(screen.get_monitor_at_window(window))

    offx, offy = offsets(window)
    w, h = (workarea.width / 4, workarea.height / 3)

    pos = (
        min(startpos[0], endpos[0]),
        min(startpos[1], endpos[1])
    )
    dims = (
        max(abs(endpos[0] - startpos[0]) + 1, 1),
        max(abs(endpos[1] - startpos[1]) + 1, 1)
    )
    window.move_resize(
        pos[1] * w,
        pos[0] * h,
        w * dims[1] - (offx * 2),
        h * dims[0]- (offx + offy)
    )

def active_window():
    screen = Gdk.Screen.get_default()
    window = screen.get_active_window()

    if no_window(screen, window):
        return None

    return (window, screen)


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
