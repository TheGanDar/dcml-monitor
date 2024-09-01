# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario Gangemi
# Student ID: 7062188
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

    This could indicate system stress due to various factors, such as CPU load spikes, abnormal CPU statistics,
    memory saturation (both swap and virtual), high disk usage, intense disk I/O operations, or heavy network traffic.
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
        end_time = time.time() + random.randint(2, 20)
        while time.time() < end_time:
            pass

    # Simulate faults for CPU Stats
    elif fault_type == 'cpu_stats':
        log_error("FAULT INJECTION: CPU Stats anomaly!")
        time.sleep(random.randint(2, 20))

    # Simulate faults for CPU Load
    elif fault_type == 'cpu_load':
        log_error("FAULT INJECTION: CPU Load spike!")
        end_time = time.time() + random.randint(2, 20)
        while time.time() < end_time:
            pass

    # Simulate faults for Swap Memory
    elif fault_type == 'swap_memory':
        log_error("FAULT INJECTION: Swap Memory exhaustion!")
        a = []
        for _ in range(10 ** 6):
            a.append(' ' * 1024) #Simulation of the allocation of an empty string of 1 MB
        time.sleep(random.randint(2, 20))
        del a

    # Simulate faults for Virtual Memory
    elif fault_type == 'virtual_memory':
        log_error("FAULT INJECTION: Virtual Memory saturation!")
        a = []
        for _ in range(10 ** 6):
            a.append(' ' * 1024) #Simulation of the allocation of an empty string of 1 MB
        time.sleep(random.randint(2, 20))
        del a

    # Simulate faults for Disk Usage
    elif fault_type == 'disk_usage':
        log_error("FAULT INJECTION: Disk Usage increase!")
        with open('temp_disk_usage.dat', 'wb') as f:
            f.write(os.urandom(1024 * 1024 * 1024))  # Write 1 GB of random data
        time.sleep(random.randint(2, 20))
        os.remove('temp_disk_usage.dat')

    # Simulate faults for Disk IO
    elif fault_type == 'disk_io':
        log_error("FAULT INJECTION: Disk IO load!")
        with open('temp_disk_io.dat', 'wb') as f:
            f.write(os.urandom(1024 * 1024 * 1024))  # Write 1 GB of random data
        with open('temp_disk_io.dat', 'rb') as f:
            while f.read(1024 * 1024 * 500):  # Read the file in 500 MB chunks
                pass
        os.remove('temp_disk_io.dat')

    # Simulate faults for Net IO
    elif fault_type == 'net_io':
        log_error("FAULT INJECTION: Net IO stress!")
        # Simulate network stress by performing a large data transfer
        with open('temp_net_io.dat', 'wb') as f:
            f.write(os.urandom(1024 * 1024 * 1024))  # Write 1 GB of random data
        os.remove('temp_net_io.dat')
