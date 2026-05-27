import time
import json
from RFID import *
from WSclient import WebSocketClient

ws = WebSocketClient("ESP32", "192.168.10.149", 8080)
print("WebSocket connected")
rfid = RFID(ws)

last_rfid_check = time.ticks_ms()
found_tag = ""

while True:
    now = time.ticks_ms()

    if time.ticks_diff(now, last_rfid_check) > 200:
        if rfid.mode == "rfid":
            # Always check for RFID tag
            rfid_tag = rfid.poll_rfid()
            last_rfid_check = time.ticks_ms()

            if rfid_tag:
                rfid.mode = "buttons"
            

        elif rfid.mode == "buttons":
            button_pressed = rfid.poll_buttons()
            # If you ever want to switch back to RFID mode after a timeout or event, do it here

    time.sleep(0.01)