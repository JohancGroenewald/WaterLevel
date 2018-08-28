import time
import led
from wifi import WiFi
from messaging import Messaging


# noinspection PyUnresolvedReferences
class RunLoop:
    def __init__(self, config, verbose=0):
        self.verbose = verbose
        if self.verbose:
            print('RunLoop: __init__')
        # ------------------------------------------------------------------------------------------------------------ #
        self.exit = False
        self.config = config
        # ------------------------------------------------------------------------------------------------------------ #
        # Initialise required services
        self.led = led.Led(self.config['pinout']['led'])
        self.wifi = WiFi(self.config, verbose=verbose)
        self.device_id = self.wifi.device_id()
        self.messaging = Messaging(self.config, self.device_id)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.verbose:
            print('<{} with id {}>'.format(self.config['device']['name'], self.device_id))
            print(str(self.led))
            print(str(self.wifi))
        # Application ready feedback --------------------------------------------------------------------------------- #
        self.led.on(poll=True)
        time.sleep(2)
        self.led.off(poll=True)
        # ------------------------------------------------------------------------------------------------------------ #

    def run(self):
        if self.verbose:
            print('Run loop started')
        while not self.exit:
            self.led.poll()
            # -------------------------------------------------------------------------------------------------------- #
            if self.wifi.connected():
                self.messaging.connect()
                self.led.toggle(500)            # Connected feedback
            elif self.wifi.connecting():
                self.led.toggle(250)            # Connected feedback
            elif not self.wifi.connected():
                self.wifi.connect()
            # -------------------------------------------------------------------------------------------------------- #

            # -------------------------------------------------------------------------------------------------------- #
            time.sleep_ms(20)                   # Reduce the tightness of the run loop
        if self.verbose:
            print('Run loop exited')

    def close(self):
        self.exit = True
        if self.led:
            self.led.close()
        # close ultrasound
        # close pump
        if self.messaging:
            self.messaging.disconnect()
        if self.wifi:
            self.wifi.disconnect()
        if self.verbose:
            print('Run loop closed')
