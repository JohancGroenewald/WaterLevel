"""
This module provides functionality for the following:
1.  Search for the current water level.
    To be done at start-up or when the water level fluctuate unreasonably
    Two
2.  Track the
"""
import time
import math
from hcsr04 import HCSR04


# noinspection PyUnresolvedReferences,PyArgumentList
class WaterLevel:
    def __init__(self, config):
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
                self.level_queue.append(new_level)
                if len(self.level_queue) > self.queue_depth:
                    self.level_queue = self.level_queue[1:]
                print(self.level_queue)
                return True
        return False

    def level(self):
        return self.level_queue[-1] if self.level_queue else -1

    def calibrated(self):
        return self._calibrated

    def close(self):
        self._calibrated = False
        self.ultrasound.trigger.value(0)
