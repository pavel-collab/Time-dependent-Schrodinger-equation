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

sigma_range = np.linspace(0.5, 5, 10)

for sigma in sigma_range:
    subprocess.run(["python3", "WavePackage.py", "-s", str(sigma)])

print("end of run")
