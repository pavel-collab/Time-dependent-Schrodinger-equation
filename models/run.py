#!/usr/bin/env python3
'''
Using subprocess module to automitic run experements one by one
'''

import subprocess
from datetime import datetime
import numpy as np

start = datetime.now()
date = datetime.strftime(start, "%d.%m.%Y-%H.%M.%S")

log_file = open('info.log', 'a')
log_file.write('-'*50 + '\n')
log_file.write(date + '\n')
log_file.write('-'*50 + '\n')
log_file.close()

E_range = np.array([0.51, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])

for E in E_range:
    subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", str(E)])

total_exec_t = datetime.now() - start

log_file = open('info.log', 'a')
log_file.write('TOTAL EXECUTE TIME: ' + str(total_exec_t) + '\n\n')
log_file.close()