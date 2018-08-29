import sys
import gc


def run():
    application = [
        'config',
        'application',
        'run',
        'led',
        'wifi',
        'waterlevel',
        'FlowRate',
        'messaging',
        'umqtt_robust',
        'umqtt_simple',
        'socket',
        'usocket',
        'network',
        'hcsr04',
        'listmodules',
        'listfiles',
        'cat',
        'done '         # Not a module. REPL feedback only
    ]
    message = 'Unloading application module ... '
    buffer = ''
    buffer_len = len(buffer)
    for module in application:
        buffer = '\r{}{}'.format(message, module)
        if len(buffer) < buffer_len:
            padding = (' ' * (buffer_len - len(buffer)))
        else:
            padding = ''
        print('{}{}'.format(buffer, padding), end='')
        if module in sys.modules:
            del sys.modules[module]
        buffer_len = len(buffer)
    print('\nRunning the GC ... ', end='')
    gc.collect()
    print('done')
    if 'unload' in sys.modules:
        del sys.modules['unload']


run()
