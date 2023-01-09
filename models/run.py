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

a_range = np.arange(1, 20)

for a in a_range:
    subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-a", str(a)])

# E_range = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49])

# for E in E_range:
#     subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", str(E)])

total_exec_t = datetime.now() - start

log_file = open('info.log', 'a')
log_file.write('TOTAL EXECUTE TIME: ' + str(total_exec_t) + '\n\n')
log_file.close()