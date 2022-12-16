'''
Using subprocess module to automitic run experements one by one
'''

import subprocess

subprocess.run(["python3", "WavePackage.py"])
subprocess.run(["python3", "HarmonicOscillator.py"])
subprocess.run(["python3", "QuantumTunnelling.py"])

print("end of run")
