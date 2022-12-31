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

subprocess.run(["python3", "BoxPit.py", "-i"])
subprocess.run(["python3", "HarmonicOscillator.py", "-i"])
subprocess.run(["python3", "QuantumTunnelling.py", "-i"])
subprocess.run(["python3", "RampPotential.py", "-i"])
subprocess.run(["python3", "StepPotential.py", "-i"])
subprocess.run(["python3", "TwoBariers.py", "-i"])
subprocess.run(["python3", "TwoLevelBoxPotential.py", "-i"])
subprocess.run(["python3", "TwoWall.py", "-i"])

print("end of run")
