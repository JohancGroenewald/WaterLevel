
class FlowRate:
    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.pulse_pin = config['pinout']['flow_meter']['pulse_pin']
        self.pulses_per_liter = config['pinout']['flow_meter']['pulses_per_liter']
        self.flow_meter = None

    def __repr__(self):
        return '<FlowRate: {}ppl at {:x}>'.format(
            self.pulses_per_liter,
            id(self)
        )
