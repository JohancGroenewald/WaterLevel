import machine
import time

print('Rebooting ESP32 ... please wait until the WebREPL becomes \'Disconnected\'')
time.sleep(2)
machine.reset()
