"""
Water Level Application

Box size: Length=120mm, Width=80mm, Height=60mm

Update history
--------------
20190825.2121: Created
"""
from config import CONFIG
import run

run_loop = run.RunLoop(CONFIG, verbose=1)
# noinspection PyBroadException
try:
    run_loop.run()
except Exception as e:
    import sys

    # noinspection PyUnresolvedReferences
    sys.print_exception(e)
finally:
    run_loop.close()

import unload
unload.run()
