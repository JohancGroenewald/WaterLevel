import os

files = [f for f in os.listdir()]
files.sort()
for f in files:
    print(f)

import sys
del sys.modules['listfiles']
