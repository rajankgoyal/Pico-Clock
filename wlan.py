# Import modules
import network, socket

def connect_WLAN(NAME, PASSWORD):
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(NAME, PASSWORD)
    while not wlan.isconnected():
        pass
    return('Connected to WLAN')

