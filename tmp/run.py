'''
The example of using subprocess module to automitic run experements
one by one
'''

import subprocess

subprocess.run(["python3", "test1.py"])
subprocess.run(["python3", "test2.py"])
subprocess.run(["python3", "test3.py"])
subprocess.run(["python3", "test4.py"])

print("end of run")
