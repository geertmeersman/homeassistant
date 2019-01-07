import paho.mqtt.client as mqtt
import common as common
import json
import time
import datetime
import configuration

try:
  retArr = {}
  retArr['buitentemperatuur']          = common.GetVData('heating.sensors.temperature.outside')
  retArr['binnentemperatuur']          = common.GetVData('heating.circuits.0.sensors.temperature.room')
  retArr['verwarmingsprogramma']       = common.GetVData('heating.circuits.0.operating.programs.active')
  retArr['verwarmingsmode']            = common.GetVData('heating.circuits.0.operating.modes.active')
  retArr['boilertemperatuur']          = common.GetVData('heating.boiler.sensors.temperature.main')
  retArr['dhwtemperatuur']             = common.GetVData('heating.dhw.temperature')
  retArr['hotWaterStoragetemperatuur'] = common.GetVData('heating.dhw.sensors.temperature.hotWaterStorage')
  retArr['programmatemperatuur']       = common.GetVData('heating.circuits.0.operating.programs.'+retArr['verwarmingsprogramma']["value"])
  retArr['Updated']                    = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
  ################################################################################################################################################
  client = mqtt.Client("Viessmann publisher")
  client.username_pw_set(configuration.mqttc['user'],configuration.mqttc['password'])
  client.connect(configuration.mqttc['broker'], 1883, 60)
  client.publish("Viessmann/status", json.dumps(retArr))
  time.sleep(2)
  client.disconnect()
  time.sleep(10)
except:
  pass
exit()

