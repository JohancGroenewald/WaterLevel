import machine

class FlowRate:
    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.pulse_pin = config['pinout']['flow_meter']['pulse_pin']
        self.pulses_per_liter = config['pinout']['flow_meter']['pulses_per_liter']
        self._calibrated = False
        self.flow_history = []
        self.flow_rate = 0.0
        self.flow_readings = 0
        self.pulse = machine.Pin(
            self.pulse_pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP
        )
        self.pulse_cycle = 0
        self.up_counter = 0

    def __repr__(self):
        return '<FlowRate: {}ppl at {:x}>'.format(
            self.pulses_per_liter,
            id(self)
        )

    def calibrated(self):
        return self._calibrated

    def calibrate(self):
        self._calibrated = True
        return self._calibrated

    # noinspection PyArgumentList
    def read(self):
        if self.pulse.value() == 0:
            if self.pulse_cycle == 0:
                self.pulse_cycle = 1
                print('--> pulse up')
        else:
            if self.pulse_cycle == 1:
                self.pulse_cycle = 0
                print('--> pulse down')
        return False

    def rate(self):
        return {
            'flow_history': self.flow_history,
            'flow_rate': self.flow_rate,
            'flow_readings': self.flow_readings
        }

    def close(self):
        self._calibrated = False
