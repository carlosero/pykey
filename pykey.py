from Xlib.display import Display
import Xlib
from Xlib import X
import Xlib.XK
import sys
import signal
import time
display = None
root = None

window_name = 'Medivia Online'
key_codes = {
    26: 111,
    39: 113,
    40: 116,
    41: 114
}

def handle_event(event):
    window = display.get_input_focus().focus
    if window.get_wm_name() == window_name:
        if event.detail in key_codes.keys():
            handle_keys(event, key_codes[event.detail])
    else:
        handle_keys(event, event.detail)

def handle_keys(event, keycode):
    if (event.type == X.KeyPress):
        send_press_key(keycode)
    if (event.type == X.KeyRelease):
        send_release_key(keycode)

# from http://shallowsky.com/software/crikey/pykey-0.1
def send_press_key(keycode):
    shift_mask = 0 # or Xlib.X.ShiftMask
    window = display.get_input_focus()._data["focus"]
    event = Xlib.protocol.event.KeyPress(
        time = int(time.time()),
        root = root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        detail = keycode
    )
    window.send_event(event, propagate = True)

def send_release_key(keycode):
    shift_mask = 0 # or Xlib.X.ShiftMask
    window = display.get_input_focus()._data["focus"]
    event = Xlib.protocol.event.KeyRelease(
        time = int(time.time()),
        root = display.screen().root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        detail = keycode
    )
    window.send_event(event, propagate = True)

def main():
    # current display
    global display,root
    display = Display()
    root = display.screen().root
    # we tell the X server we want to catch keyPress event
    root.change_attributes(event_mask = X.KeyPressMask|X.KeyReleaseMask)
    # just grab the "1"-key for now
    for key_code in key_codes.keys():
        root.grab_key(key_code, 0, True,X.GrabModeSync, X.GrabModeSync)
    signal.signal(signal.SIGALRM, lambda a,b:sys.exit(1))
    signal.alarm(10)
    while 1:
        event = display.next_event()
        handle_event(event)
        display.allow_events(X.AsyncKeyboard, X.CurrentTime)

if __name__ == '__main__':
    main()
