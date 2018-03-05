import dht
import machine
import socket
import utime
import ntptime

from settings import sensor_name, host_name
from utils import reconnect, isconnected

d = dht.DHT22(machine.Pin(4))
rtc = machine.RTC()
p0 = machine.PWM(machine.Pin(0))
p2 = machine.Pin(2)

def send_measurements(now_tup, temp, humid):
    
    #metric.path value timestamp\n
    ts = 946684800 + utime.mktime(now_tup)
    
    lines_format = 'sensor.{}.temperature {} {}\nsensor.{}.humidity {} {}\n'
    lines = lines_format.format(sensor_name, temp, ts, sensor_name, humid, ts)
    
    addr = socket.getaddrinfo(host_name, 2003)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes(lines, 'utf-8'))
    s.close()

def take_measurement():
    d.measure()
    temp = d.temperature()
    humid = d.humidity()
    return temp, humid

def setup():
    p0.freq(4)
    p0.duty(255)
    reconnect()
    ntptime.host = host_name
    ntptime.settime()

def main():
    setup()
    
    loop()
    
def loop():
    p0.freq(1)
    p0.duty(255)
    while True:
        p2.on()
        temp, humid = take_measurement()
        now_tup = utime.localtime()
        if not isconnected():
            reconnect()
        send_measurements(now_tup, temp, humid)
        if now_tup[4] == 0:
            ntptime.settime()
        to_sleep = 60 - utime.localtime()[5]
        p2.off()
        utime.sleep(to_sleep)

    #record measurements and time
    #check connected
    #connect again if needed
    #send measurements
    #update time
    #sleep time to next measurements
