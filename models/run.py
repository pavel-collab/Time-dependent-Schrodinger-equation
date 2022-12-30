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

subprocess.run(["python3", "BoxPit.py"])
subprocess.run(["python3", "HarmonicOscillator.py"])
subprocess.run(["python3", "QuantumTunnelling.py"])
subprocess.run(["python3", "RampPotential.py"])
subprocess.run(["python3", "StepPotential.py"])
subprocess.run(["python3", "TwoBariers.py"])
subprocess.run(["python3", "TwoLevelBoxPotential.py"])
subprocess.run(["python3", "TwoWall.py"])
subprocess.run(["python3", "WavePackage.py"])

subprocess.run(["python3", "BoxPit.py", "-wf", "-i"])
subprocess.run(["python3", "HarmonicOscillator.py", "-wf", "-i"])
subprocess.run(["python3", "QuantumTunnelling.py", "-wf", "-i"])
subprocess.run(["python3", "RampPotential.py", "-wf", "-i"])
subprocess.run(["python3", "StepPotential.py", "-wf", "-i"])
subprocess.run(["python3", "TwoBariers.py", "-wf", "-i"])
subprocess.run(["python3", "TwoLevelBoxPotential.py", "-wf", "-i"])
subprocess.run(["python3", "TwoWall.py", "-wf", "-i"])
subprocess.run(["python3", "WavePackage.py", "-wf", "-i"])

print("end of run")
