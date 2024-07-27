# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario
# A.A: 2023/2024

import time
import random


def simulate_fault():
    """
    Function to simulate a fault in the system.
    This could be CPU load spike and memory saturation.
    """
    fault_type = random.choice(['cpu', 'memory'])

    if fault_type == 'cpu':
        # Simulate CPU load spike by running a busy loop
        print("Simulating CPU load spike...")
        end_time = time.time() + 2  # 2 seconds spike
        while time.time() < end_time:
            pass
    elif fault_type == 'memory':
        # Simulate memory saturation
        print("Simulating memory saturation...")
        a = []
        for _ in range(10 ** 6):
            a.append(' ' * 1024)  # Allocate 1MB blocks
        del a  # Release memory