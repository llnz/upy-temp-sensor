import network
import settings

sta_if = network.WLAN(network.STA_IF)

def reconnect():
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(settings.ssid, settings.wpa_psk)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def isconnected():
    return sta_if.isconnected()
