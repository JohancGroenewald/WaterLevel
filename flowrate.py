import utime
import machine


class FlowRateMetered:
    PULSE_LOW = 0
    PULSE_HIGH = 1
    PULSE_ABANDON = 2

    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.source = 'FlowRate'
        self.channel = 'FlowRateMetered'
        self.pulse_pin = config['pinout']['flow_meter']['pulse_pin']
        self.pulses_per_liter = config['pinout']['flow_meter']['pulses_per_liter']
        self.abandon_pulse = config['pinout']['flow_meter']['abandon_pulse']
        self.pulse_high = config['pinout']['flow_meter']['pulse_high_level']
        self._calibrated = False
        self.queue_depth = 20
        self.flow_history = []
        self.flow_rate = 0.0
        self.flow_rate_lpm = 0
        self.flow_readings = 0
        self.pulse = machine.Pin(
            self.pulse_pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP
        )
        self.pulse_cycle = FlowRateRaw.PULSE_LOW
        self.start_seconds = None
        self.pulse_counter = 0
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
        return self.pulse_cycle == FlowRateRaw.PULSE_HIGH

    # noinspection PyArgumentList,PyUnresolvedReferences
    def read(self):
        if self.pulse.value() == self.pulse_high:
            if self.pulse_cycle == FlowRateRaw.PULSE_LOW:
                self.pulse_cycle = FlowRateRaw.PULSE_HIGH
                self.start = utime.ticks_ms()
                if self.verbose:
                    print('-> <Pulse up>')
                if self.start_seconds is None:
                    self.start_seconds = utime.time()
                    self.pulse_counter = 0
            elif self.pulse_cycle == FlowRateRaw.PULSE_HIGH:
                pulse_width = utime.ticks_diff(utime.ticks_ms(), self.start)
                if pulse_width > self.abandon_pulse:
                    self.pulse_cycle = FlowRateRaw.PULSE_ABANDON
                    if self.verbose:
                        print('PULSE_ABANDON after {}ms'.format(pulse_width))
            elif self.pulse_cycle == FlowRateRaw.PULSE_ABANDON:
                pass
        else:
            if self.pulse_cycle == FlowRateRaw.PULSE_HIGH:
                self.pulse_cycle = FlowRateRaw.PULSE_LOW
                self.flow_readings += 1
                self.pulse_counter += 1
                pulse_width = utime.ticks_diff(utime.ticks_ms(), self.start)
                if self.verbose:
                    print('-> <Pulse down, {}ms'.format(pulse_width))
                # >> Smoothing function
                # << Smoothing function
                self.flow_history.append(pulse_width)
                if len(self.flow_history) > self.queue_depth:
                    self.flow_history = self.flow_history[1:]
                self.flow_rate = pulse_width
                return True
            elif self.pulse_cycle == FlowRateRaw.PULSE_ABANDON:
                self.pulse_cycle = FlowRateRaw.PULSE_LOW
        if self.start_seconds and (utime.time() - self.start_seconds) > 60:
            self.flow_rate_lpm = self.pulse_counter * self.pulses_per_liter
            self.start_seconds = None
            if self.verbose:
                print('-> <FlowRate {}lpm'.format(self.flow_rate_lpm))
        return False

    def rate(self):
        return {
            'source': self.source,
            'flow_history': self.flow_history,
            'flow_rate': self.flow_rate,
            'flow_rate_lpm': self.flow_rate_lpm,
            'flow_readings': self.flow_readings
        }

    def close(self):
        self._calibrated = False


class FlowRateRaw:
    PULSE_LOW = 0
    PULSE_HIGH = 1
    PULSE_ABANDON = 2

    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.source = 'FlowRate'
        self.channel = 'FlowRateRaw'
        self.pulse_pin = config['pinout']['flow_meter']['pulse_pin']
        self.pulses_per_liter = config['pinout']['flow_meter']['pulses_per_liter']
        self.abandon_pulse = config['pinout']['flow_meter']['abandon_pulse']
        self.pulse_high = config['pinout']['flow_meter']['pulse_high_level']
        self._calibrated = False
        self.queue_depth = 20
        self.flow_history = []
        self.flow_rate = 0.0
        self.flow_readings = 0
        self.pulse = machine.Pin(
            self.pulse_pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP
        )
        self.pulse_cycle = FlowRateRaw.PULSE_LOW
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
        return self.pulse_cycle == FlowRateRaw.PULSE_HIGH

    # noinspection PyArgumentList,PyUnresolvedReferences
    def read(self):
        if self.pulse.value() == self.pulse_high:
            if self.pulse_cycle == FlowRateRaw.PULSE_LOW:
                self.pulse_cycle = FlowRateRaw.PULSE_HIGH
                self.start = utime.ticks_ms()
            elif self.pulse_cycle == FlowRateRaw.PULSE_HIGH:
                pulse_width = utime.ticks_diff(utime.ticks_ms(), self.start)
                if pulse_width > self.abandon_pulse:
                    self.pulse_cycle = FlowRateRaw.PULSE_ABANDON
                    if self.verbose:
                        print('PULSE_ABANDON after {}ms'.format(pulse_width))
            elif self.pulse_cycle == FlowRateRaw.PULSE_ABANDON:
                pass
        else:
            if self.pulse_cycle == FlowRateRaw.PULSE_HIGH:
                self.pulse_cycle = FlowRateRaw.PULSE_LOW
                self.flow_readings += 1
                pulse_width = utime.ticks_diff(utime.ticks_ms(), self.start)
                # >> Smoothing function
                # << Smoothing function
                self.flow_history.append(pulse_width)
                if len(self.flow_history) > self.queue_depth:
                    self.flow_history = self.flow_history[1:]
                self.flow_rate = pulse_width
                return True
            elif self.pulse_cycle == FlowRateRaw.PULSE_ABANDON:
                self.pulse_cycle = FlowRateRaw.PULSE_LOW
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


# noinspection PyMethodMayBeStatic
class MockFlowRate:
    def __init__(self):
        self.source = 'FlowRate'
        self.channel = 'MockFlowRate'

    def __repr__(self):
        return '<{} at {:x}>'.format(self.source, id(self))

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
            'source': self.source
        }

    def close(self):
        pass
