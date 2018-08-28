# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

# noinspection PyUnresolvedReferences
import webrepl
import wifi
import gc

from config import CONFIG

webrepl.start()
wifi.WiFi(CONFIG).connect()
gc.collect()
