#!/usr/bin/python3

import os

DIRNAME = os.path.dirname(__file__)

for fn in os.listdir(DIRNAME):
    if not fn.endswith(".cfg"):
        continue

    fn = os.path.join(DIRNAME, fn)

    with open(fn, "r") as f:
        data = f.read()
    
    with open(f"{fn.split('.')[0]}.py", "w+") as f:
        f.write(f"""\
STRINGS = '''\\
{data}
'''""")
