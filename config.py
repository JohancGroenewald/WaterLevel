"""
Global configurations

The wifi access point name can be specified using regex.
The wifi key in the CONFIG dictionary must be a list of access points.
"""
# -------------------------------------------------------------------------------------------------------------------- #
WIFI_DEVELOPMENT = ('__x[1-9]__pointer__', '_Groenewald1')

WIFI_THELAB = ('theLAB', 'theLAB!!')

MQTT_DEVELOPMENT = {
    'ip': '192.168.0.50',
    'port': 1883,
    'topic': 'water_flow'
}

MQTT_THELAB = {
    'ip': '192.168.1.32',
    'port': 0,
    'topic': 'water_flow'
}

HCSR04_DEVELOPMENT = {
    'trig_pin': 32,
    'echo_pin': 35,
    'correction': 0
}

SR04T_THELAB = {
    'trig_pin': 14,
    'echo_pin': 16,
    'correction': 0
}

SSD1306_DEVELOPMENT = {
    'clock_pin': 33,
    'data_pin': 25
}

YF201_DEVELOPMENT = {
    'pulse_pin': 34,
    'pulses_per_liter': 450,
    'abandon_pulse': 150,
    'metered': False
}

YF401_DEVELOPMENT = {
    'pulse_pin': 34,
    'pulses_per_liter': 5880,
    'abandon_pulse': 150,
    'metered': False
}

LXSG_FX_20E_THELAB = {
    'pulse_pin': 27,
    'pulses_per_liter': 1,
    'abandon_pulse': 150,
    'metered': True
}

JOJO_50LT_DRUM = {
    'model': 'JOJO 50 LT DRUM',
    'height': 510,
    'volume': 50,
    'lid_inclination': 0
}

JOJO_2500LT_MULTI_SLIM = {
    'model': 'JOJO 2500 LT MULTI SLIM',
    'height': 1960,
    'volume': 2500,
    'lid_inclination': 7
}
# -------------------------------------------------------------------------------------------------------------------- #
CONFIG_DEVKIT = {
    'name': 'WaterTankTestRig',
    'tank': JOJO_50LT_DRUM,
    'sensor_inclination': 0,
    'level_read_interval': 1,
    'flow_read_interval': 1
}

PINOUT_DEVKIT = {
    'led': 2,
    'ultrasound': HCSR04_DEVELOPMENT,
    'display': None,
    'flow_meter': YF401_DEVELOPMENT
}
# -------------------------------------------------------------------------------------------------------------------- #
CONFIG_THELAB_W1 = {
    'name': 'WaterTank1',
    'tank': JOJO_2500LT_MULTI_SLIM,
    'sensor_inclination': 0,
    'level_read_interval': 1,
    'flow_read_interval': 1
}

PINOUT_THELAB_W1 = {
    'led': None,
    'ultrasound': None,
    'display': None,
    'flow_meter': LXSG_FX_20E_THELAB
}
# -------------------------------------------------------------------------------------------------------------------- #
CONFIG = {
    'device': CONFIG_THELAB_W1,
    'pinout': PINOUT_THELAB_W1,
    'wifi': [WIFI_DEVELOPMENT, WIFI_THELAB],
    'mqtt': MQTT_DEVELOPMENT
}
# -------------------------------------------------------------------------------------------------------------------- #
