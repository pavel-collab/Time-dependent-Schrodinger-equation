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

k_range = np.array([100, 120, 130, 140, 150, 160, 170, 180, 190, 200])

for k in k_range:
    subprocess.run(["python3", "RampPotential.py", "-k", str(k)])

total_exec_t = datetime.now() - start

log_file = open('info.log', 'a')
log_file.write('TOTAL EXECUTE TIME: ' + str(total_exec_t) + '\n\n')
log_file.close()