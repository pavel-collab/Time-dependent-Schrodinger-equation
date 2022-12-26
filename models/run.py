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

k_range = [90, 110, 130, 150, 170, 190, 210, 250, 280, 320]

for k in k_range:
    subprocess.run(["python3", "RampPotential.py", "-k", str(k)])

print("end of run")
