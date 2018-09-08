import time
import led
from wifi import WiFi
from messaging import Messaging
from waterlevel import WaterLevel, MockWaterLevel
from flowrate import (
    FlowRateFallingEdge, MockFlowRate
)


# noinspection PyUnresolvedReferences
class RunLoop:
    def __init__(self, config, verbose=0):
        self.verbose = verbose
        # ------------------------------------------------------------------------------------------------------------ #
        self.exit = False
        self.config = config
        # ------------------------------------------------------------------------------------------------------------ #
        # Initialise required services
        if self.config['pinout']['led'] is None:
            self.led = led.MockLed()
        else:
            self.led = led.Led(self.config['pinout']['led'])
        self.wifi = WiFi(self.config, verbose=self.verbose)
        self.device_id = self.wifi.device_id()
        self.messaging = Messaging(self.config, self.device_id)
        if self.config['pinout']['ultrasound'] is None:
            self.water_level = MockWaterLevel()
        else:
            self.water_level = WaterLevel(self.config, verbose=self.verbose)
        if self.config['pinout']['flow_meter'] is None:
            self.flow_rate = MockFlowRate()
        else:
            self.flow_rate = FlowRateFallingEdge(self.config, verbose=self.verbose)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.verbose:
            print('<{} with id {}>'.format(self.config['device']['name'], self.device_id))
            print(self.led)
            print(self.wifi)
            print(self.messaging)
            print(self.water_level)
            print(self.flow_rate)
        # Application ready feedback --------------------------------------------------------------------------------- #
        self.led.on(poll=True)
        time.sleep(2)
        self.led.off(poll=True)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.wifi.connected():
            self.on_wifi_connected()
        # ------------------------------------------------------------------------------------------------------------ #

    def on_wifi_connected(self):
        self.led.toggle(500)
        if not self.messaging.connected():
            self.messaging.connect()

    def run(self):
        if self.verbose:
            print('Run loop started')
        while not self.exit:
            # ======================================================================================================== #
            self.led.poll()
            # -------------------------------------------------------------------------------------------------------- #
            if self.wifi.connected():
                if not self.water_level.calibrated():
                    self.water_level.calibrate()
                elif self.water_level.read():
                    self.messaging.publish(self.water_level.level())
                if not self.flow_rate.calibrated():
                    self.flow_rate.calibrate()
                elif self.flow_rate.read():
                    self.messaging.publish(self.flow_rate.rate())
            elif self.wifi.connecting():
                self.led.toggle(250)
            elif not self.wifi.connected():
                self.wifi.connect()
                if self.wifi.connected():
                    self.on_wifi_connected()
            # ======================================================================================================== #
            if self.flow_rate.reading():
                time.sleep_ms(1)
            else:
                time.sleep_ms(20)  # Reduce the tightness of the run loop
            # ======================================================================================================== #
        if self.verbose:
            print('Run loop exited')

    def close(self):
        self.exit = True
        if self.led:
            self.led.close()
        if self.water_level:
            self.water_level.close()
        if self.flow_rate:
            self.flow_rate.close()
        if self.messaging:
            self.messaging.disconnect()
        # if self.wifi:
        #     self.wifi.disconnect()            # Don't do this, you will loose connection to the REPL
        if self.verbose:
            print('Run loop closed')
