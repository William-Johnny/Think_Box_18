from time import sleep_ms
from machine import Pin, SPI
from MFRC522 import MFRC522


class RFID:
    def __init__(self, wsClient):
        # SPI setup
        self.sck = Pin(18, Pin.OUT)
        self.mosi = Pin(23, Pin.OUT)
        self.miso = Pin(19, Pin.OUT)

        self.spi = SPI(
            baudrate=100000,
            polarity=0,
            phase=0,
            sck=self.sck,
            mosi=self.mosi,
            miso=self.miso
        )

        # RFID CS pin
        self.cs_pin = Pin(5, Pin.OUT)

        # RFID reader
        self.reader = MFRC522(self.spi, self.cs_pin)

        # Buttons
        self.buttons = [
            {
                "optionId": "one",
                "pin": Pin(14, Pin.IN, Pin.PULL_UP),
                "pressed": False
            },
            {
                "optionId": "two",
                "pin": Pin(25, Pin.IN, Pin.PULL_UP),
                "pressed": False
            },
        ]

        self.wsClient = wsClient
        self.sendToESP = True
        self.mode = "rfid"
        self.currentUID = ""

    def check_reader(self):
        (stat, tag_type) = self.reader.request(self.reader.REQIDL)

        if stat == self.reader.OK:
            (stat, raw_uid) = self.reader.anticoll()

            if stat == self.reader.OK:
                uid = "0x%02x%02x%02x%02x" % tuple(raw_uid[:4])

                print("RFID detected:", uid)
                self.currentUID = uid

                self.wsClient.send("HTMLPage", uid, "")

                return True

        return False

    def check_buttons(self):
        for btn in self.buttons:
            if not btn["pin"].value() and not btn["pressed"]:
                btn["pressed"] = True
                return btn["optionId"]
            elif btn["pin"].value():
                btn["pressed"] = False
        return None

    def poll_buttons(self):
        btnOption = self.check_buttons()

        if btnOption:
            print(f"Detected button: {btnOption}")

            self.wsClient.send(
                "HTMLPage",
                self.currentUID,
                btnOption
            )

    def poll_rfid(self):
        if self.check_reader():
            return True

        return False
