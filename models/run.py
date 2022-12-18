'''
Using subprocess module to automitic run experements one by one
'''

import subprocess
from datetime import datetime

date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")

log_file = open('info.log', 'a')
log_file.write('-'*50 + '\n')
log_file.write(date + '\n')
log_file.write('-'*50 + '\n')
log_file.close()

subprocess.run(["python3", "RampPotential.py"])
subprocess.run(["python3", "StepPotential.py"])
subprocess.run(["python3", "TwoLevelBoxPotential.py"])

print("end of run")
