# homeassistant Viessmann integration
home-assistant.io

# Viessmann scripts
This folder contains scripts to connect to the ViCare service (for eg Viessmann gas boilers) and allows to read out all interesting information and publish it on the MQTT broker.
It also contains a listener which subscribes to the MQTT and can change the Viessmann active mode.

I run the mqttlistener script in a daemon mode : sudo python /home/pi/python_scripts/mqttlistener.py &

The viessmannToMQTT script runs every minute (crontab job): python /home/pi/python_scripts/viessmannToMQTT.py

The configuration.py contains the credentials of Viessmann and the MQTT broker.

# TODO
Creating a home assistant component
Improve some error handling (but not critical now)

# Integration in home assistant
You can easily integrate this into home assistant by creating the following 

sensors:
```
- platform: mqtt
  name: "Buitentemperatuur"
  state_topic: "Viessmann/status"
  unit_of_measurement: '°C'
  value_template: "{{ value_json.buitentemperatuur.value }}"
- platform: mqtt
  name: "Binnentemperatuur"
  state_topic: "Viessmann/status"
  unit_of_measurement: '°C'
  value_template: "{{ value_json.binnentemperatuur.value }}"
- platform: mqtt
  name: "Verwarmingsmode"
  state_topic: "Viessmann/status"
  value_template: "{{ value_json.verwarmingsmode.value }}"
- platform: mqtt
  name: "Verwarmingsprogramma"
  state_topic: "Viessmann/status"
  value_template: "{{ value_json.verwarmingsprogramma.value }}"
- platform: mqtt
  name: "Programmatemperatuur"
  state_topic: "Viessmann/status"
  unit_of_measurement: '°C'
  value_template: "{{ value_json.programmatemperatuur.temperature }}"
- platform: mqtt
  name: "Boilertemperatuur"
  state_topic: "Viessmann/status"
  unit_of_measurement: '°C'
  value_template: "{{ value_json.boilertemperatuur.value }}"
- platform: mqtt
  name: "Warm-watertemperatuur"
  state_topic: "Viessmann/status"
  unit_of_measurement: '°C'
  value_template: "{{ value_json.hotWaterStoragetemperatuur.value }}"
- platform: mqtt
  name: "Warm-watertemperatuur (doel)"
  state_topic: "Viessmann/status"
  unit_of_measurement: '°C'
  value_template: "{{ value_json.dhwtemperatuur.value }}"
- platform: mqtt
  name: "Status tijdstip"
  icon_template: mdi:update
  state_topic: "Viessmann/status"
  value_template: "{{ value_json.Updated }}"
- platform: mqtt
  name: "Listener tijdstip"
  icon_template: mdi:update
  state_topic: "Viessmannlistener/lastseen"
```

input_select:
```
viessmann_mode:
  name: Mode
  icon: mdi:target
  options:
    - "Uit"
    - "Enkel warm water"
    - "Verwarming en warm water"
    - "Permanent verlaagd"
    - "Continu dagwerking"
```

automations:
```
###########
# HVAC
###########

- alias: Set Viessman Mode
  trigger:
    platform: state
    entity_id: input_select.viessmann_mode
  action:
    service: mqtt.publish
    data_template:
      topic: "Viessmann/mode"
      retain: true
      payload: "{{ states('input_select.viessmann_mode') }}"
```
