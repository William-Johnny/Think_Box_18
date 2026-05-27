import network
import time
# Configuration Wi-Fi
SSID = "Cudy-FA5C"
PASSWORD = "58448069"
# Connexion au Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connexion au réseau Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connecté au Wi-Fi :", wlan.ifconfig())
    
connect_wifi()