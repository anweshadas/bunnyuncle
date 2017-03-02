import utime
from umqtt.simple import MQTTClient
import machine
import pca9685


pin0 = machine.Pin(0, machine.Pin.OUT)
pin2 = machine.Pin(2, machine.Pin.OUT)


def sub_cb(topic,msg):
    i2c = machine.I2C(-1, machine.Pin(14), machine.Pin(4))
    pca = pca9685.PCA9685(i2c)
    pca.freq(240)
    for x in range(0,5):
        pca.duty(x,32)

def stop_light():
    i2c = machine.I2C(-1, machine.Pin(14), machine.Pin(4))
    pca = pca9685.PCA9685(i2c)
    pca.freq(240)
    for x in range(0, 5):
        pca.duty(x, 0)

def main(server="192.168.1.1"):
    utime.sleep(5)
    c = MQTTClient("umqtt_client", server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"bunnyuncle/msg")
    magicGPIO = 13
    magicbtn = machine.Pin(magicGPIO, machine.Pin.IN, machine.Pin.PULL_UP)
    while True:
        c.check_msg()
        utime.sleep(2)
        if magicbtn.value() == 0:
            stop_light()

    c.disconnect()


main()