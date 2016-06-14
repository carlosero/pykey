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
    26: 111, # e
    39: 113, # s
    40: 116, # d
    41: 114, # f
    25: 79,  # w
    27: 81,  # r
    53: 87,  # x
    55: 89   # v
}
ctrl_codes = [26,39,40,41]
KEY_SWITCHER = 36 # key for switching on-off the key remaping
detection_enabled = True

def handle_event(event):
    global detection_enabled
    window = display.get_input_focus().focus
    if window.get_wm_name() == window_name:
        if event.type == X.KeyRelease and event.state == 4 and event.detail == KEY_SWITCHER:
            detection_enabled = not detection_enabled
        if event.detail in ctrl_codes and detection_enabled and event.state == 4:
            send_press_key(key_codes[event.detail], event.state)
            send_release_key(key_codes[event.detail], event.state)
        else:
            if event.detail in key_codes.keys() and detection_enabled:
                handle_keys(event, key_codes[event.detail], event.state)
            else:
                handle_keys(event, event.detail, event.state)
    else:
        handle_keys(event, event.detail, event.state)

def handle_keys(event, keycode, state = 0):
    if (event.type == X.KeyPress):
        send_press_key(keycode, state)
    if (event.type == X.KeyRelease):
        send_release_key(keycode, state)

# from http://shallowsky.com/software/crikey/pykey-0.1
def send_press_key(keycode, state = 0):
    window = display.get_input_focus()._data["focus"]
    event = Xlib.protocol.event.KeyPress(
        time = int(time.time()),
        root = root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = state,
        detail = keycode
    )
    window.send_event(event, propagate = True)

def send_release_key(keycode, state = 0):
    window = display.get_input_focus()._data["focus"]
    event = Xlib.protocol.event.KeyRelease(
        time = int(time.time()),
        root = display.screen().root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = state,
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
    # Common keys without state
    for key_code in key_codes.keys():
        root.grab_key(key_code, 0, True,X.GrabModeSync, X.GrabModeSync)
    # Keys with shift
    for key_code in ctrl_codes:
        root.grab_key(key_code, 4, True,X.GrabModeSync, X.GrabModeSync)
    # Switcher key
    root.grab_key(KEY_SWITCHER, 4, True,X.GrabModeSync, X.GrabModeSync)
    signal.signal(signal.SIGALRM, lambda a,b:sys.exit(1))
    signal.alarm(30)
    while 1:
        event = display.next_event()
        handle_event(event)
        display.allow_events(X.AsyncKeyboard, X.CurrentTime)

if __name__ == '__main__':
    main()
