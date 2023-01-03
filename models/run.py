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

# compare step potential model with E < U and E > U
subprocess.run(["python3", "StepPotential.py", "-i"])
subprocess.run(["python3", "StepPotential.py", "-i", "-e", "1"])

# En for TwoBariers
subprocess.run(["python3", "TwoBariers.py", "-i"])              # not En
subprocess.run(["python3", "TwoBariers.py", "-i", "-e", "0.6"]) # not En
subprocess.run(["python3", "TwoBariers.py", "-i", "-e", "0.8"]) # not En
subprocess.run(["python3", "TwoBariers.py", "-i", "-e", "0.0002"])
subprocess.run(["python3", "TwoBariers.py", "-i", "-e", "0.0219"])
subprocess.run(["python3", "TwoBariers.py", "-i", "-e", "0.548"])

subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", "0.3"]) # E < U
subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", "0.4"]) # E < U
subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", "0.5"]) # E = U
subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", "0.8"]) # E > U
subprocess.run(["python3", "QuantumTunnelling.py", "-i", "-e", "1"]) # E > U

# sigma stepping

# test sigma stepping sigma > 5.0
sigma_range = np.array([5, 7, 9, 11, 15])

for sigma in sigma_range:
    subprocess.run(["python3", "TwoLevelBoxPotential.py", "-i", "-s", str(sigma)])

total_exec_t = datetime.now() - start

log_file = open('info.log', 'a')
log_file.write('total execute time: ' + str(total_exec_t) + '\n')
log_file.write('='*50 + '\n')
log_file.close()