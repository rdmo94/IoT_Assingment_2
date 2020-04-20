import sys
import time
import base64
from encodings.utf_8 import decode

from bitstring import BitArray
import paho.mqtt.client as mqtt

broker="influx.itu.dk"
dataRaw = open("dataRaw.txt", "w+")
dataFormatted = open("dataFormatted.txt", "w+")

def on_log(client, userdata, level, buf):
    print("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK")

    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    decodedMsg = base64.decodebytes(message.payload)
    byteZeroRaw = decodedMsg[0]
    byteZero = bin(byteZeroRaw)[2:]
    isRandom = byteZero[0]
    id = int("0" + byteZero[1:], 2)
    timestamp = decodedMsg[1:5]
    data = decodedMsg[5:]

    isRandomText = "Is Data Randomly Generated? " + str(isRandom)
    idText = "ID: " + str(id)
    unixTimeStampText = "UNIX Timestamp: " + str(int.from_bytes(timestamp, byteorder='big'))
    dataMwhText = "Data (MWh): " + str(int.from_bytes(data, byteorder='big'))

    rawLines = isRandom + " - " + idText + " - " + unixTimeStampText + " - " + dataMwhText + "\n"
    formattedLines = isRandomText + "\n" + idText + "\n" + unixTimeStampText + "\n" + dataMwhText

    print("MESSAGE RECEIVED")
    print(isRandomText)
    print(idText)
    print(unixTimeStampText)
    print(dataMwhText)

    if isRandom == 0:
        dataFormatted.write(formattedLines)
        dataRaw.write(rawLines)

    # print(base64.decodebytes(message.payload))

    # print("Message received: Id" + str(id))
    # print("Message received: Timestamp1" + str(timestamp1))
    # print("Message received: Timestamp2" + str(timestamp2))
    # print("Message received: Timestamp3" + str(timestamp3))
    # print("Message received: Timestamp4" + str(timestamp4))
    # print("Message received: Data1" + str(data1))
    # print("Message received: Data2" + str(data2))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to IoT2020sec/meters")

def on_disconnect(clinet, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

cl = mqtt.Client("python1")
cl.reinitialise()
print("Client created")
cl.on_connect = on_connect
cl.on_log = on_log
cl.on_message = on_message
cl.on_subscribe = on_subscribe
cl.on_disconnect = on_disconnect
cl.username_pw_set("smartreader", password="4mp3r3h0ur")
print("username and pw set")
cl.tls_set("/Users/rdmo/Downloads/test2.pem")
cl.connect(broker, port=8883)
time.sleep(4)
cl.subscribe("IoT2020sec/meters")
print("Loop started")
cl.loop_forever()

#
# cl.loop_stop()
# cl.disconnect()







