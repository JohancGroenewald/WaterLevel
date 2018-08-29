import time
import math
from hcsr04 import HCSR04


# noinspection PyUnresolvedReferences,PyArgumentList
class WaterLevel:
    def __init__(self, config, verbose=0):
        self.verbose = verbose
        self.config = config
        self.ultrasound = HCSR04(
            trigger_pin=config['pinout']['ultrasound']['trig_pin'],
            echo_pin=config['pinout']['ultrasound']['echo_pin']
        )
        self.tank_model = config['device']['tank']['model']
        self.tank_height = config['device']['tank']['height']
        self.tank_volume = config['device']['tank']['volume']
        self.lid_inclination = config['device']['tank']['lid_inclination']
        self.read_interval = config['device']['read_interval_in_seconds']
        self.start = None
        self.level_queue = []
        self.queue_depth = 10
        self.calibration_depth = 100
        self._calibrated = False
        self.level_average = 0
        self.level_percentile = 0.0
        self.level_volume = 0

    def __repr__(self):
        return '<WaterLevel: {}, {}mm, {}L at {:x}>'.format(
            self.tank_model,
            self.tank_height,
            self.tank_volume,
            id(self)
        )

    def calibrate(self):
        self._calibrated = True
        return self._calibrated

    def read(self):
        if not self._calibrated:
            return False
        if self.start is None:
            self.start = time.time()
        else:
            ticked = time.time()
            interval = ticked - self.start
            if interval >= self.read_interval:
                self.start = ticked
                new_level = self.tank_height - self.ultrasound.distance_mm()
                new_level = 0 if new_level < 0 else self.tank_height if new_level > self.tank_height else new_level
                # >> Smoothing function
                if self.level_queue and abs(new_level - self.level_queue[-1]) > self.queue_depth:
                    new_level = self.level_queue[-1]
                # << Smoothing function
                self.level_queue.append(new_level)
                if len(self.level_queue) > self.queue_depth:
                    self.level_queue = self.level_queue[1:]
                # >> Smoothing function
                delta = (max(self.level_queue) - min(self.level_queue))
                deltas = [
                    max(self.level_queue) - level
                    for level in self.level_queue
                ]
                # << Smoothing function
                self.level_average = sum(self.level_queue) / len(self.level_queue)
                self.level_percentile = self.level_average / self.tank_height
                self.level_volume = self.tank_volume * self.level_percentile
                if self.verbose:
                    print('{}, avg: {}, per: {}, vol: {}, d: {}'.format(
                        self.level_queue, self.level_average, self.level_percentile, self.level_volume,
                        delta
                    ))
                    print(deltas)
                return True
        return False

    def level(self):
        return {
            'level_history': self.level_queue,
            'level_average': self.level_average,
            'level_percentile': self.level_percentile,
            'level_volume': self.level_volume
        }

    def calibrated(self):
        return self._calibrated

    def close(self):
        self._calibrated = False
        self.ultrasound.trigger.value(0)
