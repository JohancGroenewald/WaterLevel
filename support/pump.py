import sys
import machine
import time


def run(seconds=15):
    print('Initialise relay pin ... ', end='')
    pump=machine.Pin(12, machine.Pin.OUT)
    print('done')

    print('Turning the pump on ... ', end='')
    pump.on()
    print('done')

    for i in range(seconds):
        print('\rRunning the pump for {}/{} seconds'.format(i+1, seconds), end='')
        time.sleep(1)

    print()
    print('Turning the pump off ... ', end='')
    pump.off()
    print('done')

    if 'pump' in sys.modules:
        del sys.modules['pump']
