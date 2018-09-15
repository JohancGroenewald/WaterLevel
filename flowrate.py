import utime
import machine


class FlowRate:
    PULSE_LOW = 0
    PULSE_HIGH = 1
    PULSE_ABANDON = 2
    PULSE_TIMEOUT = 3


class FlowRateFallingEdge(FlowRate):

    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.source = 'FlowRate'
        self.channel = 'FlowRateFallingEdge'
        self.pulse_pin = config['pinout']['flow_meter']['pulse_pin']
        self.pulses_per_liter = config['pinout']['flow_meter']['pulses_per_liter']
        self.pulse_high = config['pinout']['flow_meter']['pulse_high_level']
        self._calibrated = False
        self.queue_depth = 60
        self.flow_history = []
        self.flow_rate = 0.0
        self.flow_readings = 0
        self.pulse = machine.Pin(
            self.pulse_pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP
        )
        self.pulse_cycle = self.PULSE_LOW
        self.start_seconds = None
        self.pulse_counter = 0
        self.start = 0

    def __repr__(self):
        return '<{}: {}ppl at {:x}>'.format(
            self.channel,
            self.pulses_per_liter,
            id(self)
        )

    def calibrated(self):
        return self._calibrated

    def calibrate(self):
        self._calibrated = True
        return self._calibrated

    def reading(self):
        return self.pulse_cycle == self.PULSE_HIGH

    # noinspection PyArgumentList,PyUnresolvedReferences
    def read(self):
        if self.pulse.value() == self.pulse_high:
            if self.pulse_cycle == self.PULSE_LOW:
                self.pulse_cycle = self.PULSE_HIGH
                self.start = utime.ticks_ms()
                if self.verbose:
                    print('<Pulse: UP>')
                if self.start_seconds is None:
                    self.start_seconds = utime.time()
                    self.pulse_counter = 0
        else:
            if self.pulse_cycle == self.PULSE_HIGH:
                self.pulse_cycle = self.PULSE_LOW
                self.flow_readings += 1
                self.pulse_counter += 1
                pulse_width = utime.ticks_diff(utime.ticks_ms(), self.start)
                if self.verbose:
                    print('<Pulse: DOWN after {}ms>'.format(pulse_width))
                # >> Smoothing function
                # << Smoothing function
        seconds = utime.time()
        if self.start_seconds and (seconds - self.start_seconds) > 60:
            self.flow_rate = self.pulse_counter * self.pulses_per_liter
            self.flow_history.append(self.flow_rate)
            if len(self.flow_history) > self.queue_depth:
                self.flow_history = self.flow_history[1:]
            self.start_seconds = seconds
            self.pulse_counter = 0
            if self.verbose:
                print('<FlowRate {}lpm>'.format(self.flow_rate))
            return True
        return False

    def rate(self):
        return {
            'source': self.source,
            'channel': self.channel,
            'flow_history': self.flow_history,
            'flow_rate': self.flow_rate,
            'flow_readings': self.flow_readings
        }

    def close(self):
        self._calibrated = False


# noinspection PyMethodMayBeStatic
class MockFlowRate:
    def __init__(self):
        self.source = 'FlowRate'
        self.channel = 'MockFlowRate'

    def __repr__(self):
        return '<{} at {:x}>'.format(self.channel, id(self))

    def calibrated(self):
        return True

    def calibrate(self):
        return True

    def reading(self):
        return False

    # noinspection PyArgumentList,PyUnresolvedReferences
    def read(self):
        return False

    def rate(self):
        return {
            'source': self.source,
            'channel': self.channel
        }

    def close(self):
        pass
