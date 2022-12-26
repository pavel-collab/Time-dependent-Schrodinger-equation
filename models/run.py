#!/usr/bin/env python3
'''
Using subprocess module to automitic run experements one by one
'''

import subprocess
from datetime import datetime
import numpy as np

date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")

log_file = open('info.log', 'a')
log_file.write('-'*50 + '\n')
log_file.write(date + '\n')
log_file.write('-'*50 + '\n')
log_file.close()

omega_range = [20, 24, 28, 32, 36, 40, 44]

for omega in omega_range:
    subprocess.run(["python3", "HarmonicOscillator.py", "-o", str(omega)])

print("end of run")
