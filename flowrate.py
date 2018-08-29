import utime
import machine


class FlowRate:
    PULSE_LOW = 0
    PULSE_HIGH = 1
    PULSE_ABANDON = 2

    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.source = 'FlowRate'
        self.pulse_pin = config['pinout']['flow_meter']['pulse_pin']
        self.pulses_per_liter = config['pinout']['flow_meter']['pulses_per_liter']
        self._calibrated = False
        self.queue_depth = 10
        self.flow_history = []
        self.flow_rate = 0.0
        self.flow_readings = 0
        self.pulse = machine.Pin(
            self.pulse_pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP
        )
        self.pulse_cycle = FlowRate.PULSE_LOW
        self.start = 0

    def __repr__(self):
        return '<{}: {}ppl at {:x}>'.format(
            self.source,
            self.pulses_per_liter,
            id(self)
        )

    def calibrated(self):
        return self._calibrated

    def calibrate(self):
        self._calibrated = True
        return self._calibrated

    def reading(self):
        return self.pulse_cycle == FlowRate.PULSE_HIGH

    # noinspection PyArgumentList
    def read(self):
        if self.pulse.value() == 0:
            if self.pulse_cycle == FlowRate.PULSE_LOW:
                self.pulse_cycle = FlowRate.PULSE_HIGH
                self.start = utime.ticks_ms()
            elif self.pulse_cycle == FlowRate.PULSE_HIGH:
                pulse_width = utime.ticks_ms() - self.start
                if pulse_width > 100:
                    self.pulse_cycle = FlowRate.PULSE_ABANDON
                    if self.verbose:
                        print('PULSE_ABANDON after {}ms'.format(pulse_width))
            elif self.pulse_cycle == FlowRate.PULSE_ABANDON:
                pass
        else:
            if self.pulse_cycle == FlowRate.PULSE_HIGH:
                self.pulse_cycle = FlowRate.PULSE_LOW
                self.flow_readings += 1
                pulse_width = utime.ticks_ms() - self.start
                # >> Smoothing function
                # << Smoothing function
                self.flow_history.append(pulse_width)
                if len(self.flow_history) > self.queue_depth:
                    self.flow_history = self.flow_history[1:]
                self.flow_rate = pulse_width
                return True
            elif self.pulse_cycle == FlowRate.PULSE_ABANDON:
                self.pulse_cycle = FlowRate.PULSE_LOW
        return False

    def rate(self):
        return {
            'source': self.source,
            'flow_history': self.flow_history,
            'flow_rate': self.flow_rate,
            'flow_readings': self.flow_readings
        }

    def close(self):
        self._calibrated = False