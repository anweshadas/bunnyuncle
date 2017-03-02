import time
import paho.mqtt.client as mqtt

def send_messages():
    mqttc = mqtt.Client()
    mqttc.connect("192.168.1.11", 1883, 60)
    mqttc.loop_start()
    mqttc.publish("bunnyuncle/msg", 1, 2)
    mqttc.loop_stop()
    mqttc.disconnect()

if __name__ == "__main__":
    send_messages()

