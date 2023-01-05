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

subprocess.run(["python3", "WavePackageCompare.py"])
subprocess.run(["python3", "WavePackageCompare.py", "-i", "-wf"])

subprocess.run(["python3", "BoxPitCompare.py"])
subprocess.run(["python3", "BoxPitCompare.py", "-i", "-wf"])

subprocess.run(["python3", "QuantumTunnellingCompare.py"])
subprocess.run(["python3", "QuantumTunnellingCompare.py", "-i", "-wf"])

total_exec_t = datetime.now() - start

log_file = open('info.log', 'a')
log_file.write('TOTAL EXECUTE TIME: ' + str(total_exec_t) + '\n\n')
log_file.close()