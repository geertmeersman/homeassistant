import paho.mqtt.client as mqtt
import common as common
import datetime
import configuration

def on_connect(client, userdata, flags, rc):
    client.subscribe('Viessmann/#')

def on_message(client, userdata, msg):
    try:
      common.getToken();
      print(msg)
      if msg.topic == "Viessmann/insidetemperature/set":
         setTemp(msg.payload)
      elif msg.topic == "Viessmann/mode":
         setActiveMode(msg.payload)
      client.publish("Viessmannlistener/lastseen",'{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    except:
      pass

def setTemp(temp):
	#TODO
	print("Set temperatuur to "+temp)

def setActiveMode(mode):
    if mode == "Uit":
       vMode = "standby"
    elif mode == "Enkel warm water":
       vMode = "dhw"
    elif mode == "Verwarming en warm water":
       vMode = "dhwAndHeating"
    elif mode == "Permanent verlaagd":
       vMode = "forcedReduced"
    elif mode == "Continu dagwerking":
       vMode = "forcedNormal"
    aMode = common.GetVData('heating.circuits.0.operating.modes.active')
    aMode = aMode['value']
    if aMode != vMode:
        common.SetVData('operating.modes.active', 'setMode', {"mode":vMode})

while True:
    try:
	client = mqtt.Client("Viessmann Listener")
	client.on_connect = on_connect
	client.on_message = on_message
	client.username_pw_set(configuration.mqttc['user'],configuration.mqttc['password'])
	client.connect(configuration.mqttc['broker'], 1883, 60)
	client.loop_forever()
	mqttc.disconnect()
    except:
        pass
    sleep(10)
