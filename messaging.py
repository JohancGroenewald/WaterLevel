from umqtt_robust import MQTTClient


class Messaging:
    def __init__(self, config, device_id):
        self.config = config
        self.device_id = device_id
        self.mqtt = None

    def __repr__(self):
        return '<Messaging: {}, {}, {}:{} at {:x}>'.format(
            self.device_id,
            'MQTT',
            self.config['mqtt']['ip'],
            self.config['mqtt']['port'],
            id(self)
        )

    def connect(self):
        if self.mqtt is None:
            self.mqtt = MQTTClient(
                client_id=self.device_id, server=self.config['mqtt']['ip'], port=self.config['mqtt']['port']
            )
            self.mqtt.connect()
            self.publish('{} connected'.format(self.config['device']['name']))

    def publish(self, message):
        self.mqtt.publish(self.config['mqtt']['topic'], message)

    def disconnect(self):
        if self.mqtt:
            self.mqtt.publish(
                self.config['mqtt']['topic'], '{} disconnected'.format(self.config['device']['name'])
            )
            self.mqtt.disconnect()
            self.mqtt = None

    def connected(self):
        return self.mqtt is not None
