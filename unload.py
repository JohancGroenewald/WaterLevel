import sys
import gc


def run():
    system_modules = [
        # 'config',
        # 'config_local',
        'flashbdev',
        # 'network',
        # 'socket',
        'webrepl',
        'webrepl_cfg',
        'websocket_helper',
        # 'wifi',
        'unload',
        'done '         # Not a module. REPL feedback only
    ]
    message = 'Unloading application module ... '
    buffer = ''
    buffer_len = len(buffer)
    for module in sys.modules:
        buffer = '\r{}{}'.format(message, module)
        if len(buffer) < buffer_len:
            padding = (' ' * (buffer_len - len(buffer)))
        else:
            padding = ''
        print('{}{}'.format(buffer, padding), end='')
        if module not in system_modules:
            del sys.modules[module]
        buffer_len = len(buffer)
    print('\nRunning the GC ... ', end='')
    gc.collect()
    print('done')
    if 'unload' in sys.modules:
        del sys.modules['unload']


run()
