# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario
# A.A: 2023/2024

import time
import random
import os
from datetime import datetime

error_file = '../../Dataset/error_log.txt'

def log_error(message: str, error_filename: str = error_file):
    """
    Function to log an error message with a timestamp to a text file.

    :param message: The error message to be logged.
    :param filename: The name of the log file. Defaults to 'error_log.txt'.
    """

    with open(error_filename, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}\n"
        file.write(log_entry)

def simulate_fault():
    """
    Function to simulate a fault in the system.
    This could be CPU load spike and memory saturation.
    """
    fault_type = random.choice(['cpu_times',
                                'cpu_stats',
                                'cpu_load',
                                'swap_memory',
                                'virtual_memory',
                                'disk_usage',
                                'disk_io',
                                'net_io'])

    # Simulate faults for CPU Times
    if fault_type == 'cpu_times':
        log_error("FAULT INJECTION: CPU Times spike!")
        end_time = time.time() + 2
        while time.time() < end_time:
            pass

    # Simulate faults for CPU Stats
    elif fault_type == 'cpu_stats':
        log_error("FAULT INJECTION: CPU Stats anomaly!")
        time.sleep(2)

    # Simulate faults for CPU Load
    elif fault_type == 'cpu_load':
        log_error("FAULT INJECTION: CPU Load spike!")
        end_time = time.time() + 2
        while time.time() < end_time:
            pass

    # Simulate faults for Swap Memory
    elif fault_type == 'swap_memory':
        log_error("FAULT INJECTION: Swap Memory exhaustion!")
        a = []
        for _ in range(10 ** 6):
            a.append(' ' * 1024)
        time.sleep(2)
        del a

    # Simulate faults for Virtual Memory
    elif fault_type == 'virtual_memory':
        log_error("FAULT INJECTION: Virtual Memory saturation!")
        a = []
        for _ in range(10 ** 6):
            a.append(' ' * 1024)
        time.sleep(2)
        del a

    # Simulate faults for Disk Usage
    elif fault_type == 'disk_usage':
        log_error("FAULT INJECTION: Disk Usage increase!")
        with open('temp_disk_usage.dat', 'wb') as f:
            f.write(os.urandom(1024 * 1024 * 100))  # Write 100 MB of random data
        time.sleep(2)
        os.remove('temp_disk_usage.dat')

    # Simulate faults for Disk IO
    elif fault_type == 'disk_io':
        log_error("FAULT INJECTION: Disk IO load!")
        with open('temp_disk_io.dat', 'wb') as f:
            f.write(os.urandom(1024 * 1024 * 100))  # Write 100 MB of random data
        with open('temp_disk_io.dat', 'rb') as f:
            while f.read(1024 * 1024):  # Read the file in 1 MB chunks
                pass
        os.remove('temp_disk_io.dat')

    # Simulate faults for Net IO
    elif fault_type == 'net_io':
        log_error("FAULT INJECTION: Net IO stress!")
        # Simulate network stress by performing a large data transfer
        start_time = time.time()
        with open('temp_net_io.dat', 'wb') as f:
            f.write(os.urandom(1024 * 1024 * 100))  # Write 100 MB of random data
        end_time = time.time()
        duration = end_time - start_time
        os.remove('temp_net_io.dat')















    # Simulate CPU load spike by running a busy loop
    #if fault_type == 'cpu':
    #    log_error("FAULT INJECTION: CPU load spike!")
    #    end_time = time.time() + 2  # 2 seconds spike
    #    while time.time() < end_time:
    #        pass
#
    ## Simulate memory saturation
    #elif fault_type == 'memory':
    #    log_error("FAULT INJECTION: memory saturation!")
    #    a = []
    #    for _ in range(10 ** 6):
    #        a.append(' ' * 1024)  # Allocate 1MB blocks
    #    del a  # Release memory