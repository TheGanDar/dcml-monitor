# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario Gangemi
# Student ID: 7062188
# A.A: 2023/2024

import sys
import csv
import os.path
import random
import time
from datetime import datetime
from collections import Counter
import psutil
from tqdm import tqdm
from multiprocessing import Process

from Fault_injection import simulate_fault, log_error
sys.path.append(os.path.abspath("../02 - Data Analysis"))
from Analysis_Model import model_selection, delete_pkl_file

def monitor_data():
    """
    Function to monitor the state of the system at current time
    :return: a dictionary containing couples <indicator, value>
    """
    python_data = {}

    # Adding timestamp
    python_data['timestamp'] = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # CPU Times
    tag = 'cpu_times'
    pp_data = psutil.cpu_times()
    if pp_data is not None:
        pp_dict = pp_data._asdict()
        for pp_key in pp_dict.keys():
            python_data[tag + '.' + pp_key] = pp_dict[pp_key]

    # CPU Stats
    tag = 'cpu_stats'
    pp_data = psutil.cpu_stats()
    if pp_data is not None:
        pp_dict = pp_data._asdict()
        for pp_key in pp_dict.keys():
            python_data[tag + '.' + pp_key] = pp_dict[pp_key]

    # CPU Load
    f_obj = getattr(psutil, "getloadavg", None)
    if callable(f_obj):
        tag = 'cpu_load'
        pp_data = psutil.getloadavg()
        if pp_data is not None and isinstance(pp_data, tuple) and len(pp_data) == 3:
            python_data[tag + ".load_1m"] = pp_data[0]
            python_data[tag + ".load_5m"] = pp_data[1]
            python_data[tag + ".load_15m"] = pp_data[2]

    # Swap Memory
    tag = 'swap'
    pp_data = psutil.swap_memory()
    if pp_data is not None:
        pp_dict = pp_data._asdict()
        for pp_key in pp_dict.keys():
            python_data[tag + '.' + pp_key] = pp_dict[pp_key]

    # Virtual Memory
    tag = 'virtual'
    pp_data = psutil.virtual_memory()
    if pp_data is not None:
        pp_dict = pp_data._asdict()
        for pp_key in pp_dict.keys():
            python_data[tag + '.' + pp_key] = pp_dict[pp_key]

    # Disk
    tag = 'disk'
    pp_data = psutil.disk_usage('/')
    if pp_data is not None:
        pp_dict = pp_data._asdict()
        for pp_key in pp_dict.keys():
            python_data[tag + '.' + pp_key] = pp_dict[pp_key]

    # Disk IO
    try:
        tag = 'disk_io'
        pp_data = psutil.disk_io_counters()
        if pp_data is not None:
            pp_dict = pp_data._asdict()
            for pp_key in pp_dict.keys():
                python_data[tag + '.' + pp_key] = pp_dict[pp_key]
    except:
        err = 1

    # Net IO
    tag = 'net_io'
    pp_data = psutil.net_io_counters()
    if pp_data is not None:
        pp_dict = pp_data._asdict()
        for pp_key in pp_dict.keys():
            python_data[tag + '.' + pp_key] = pp_dict[pp_key]

    return python_data


def main_monitor(out_filename : str, max_n_obs : int, obs_interval_sec : int):
    """
    Main function for monitoring
    :param obs_interval_sec: seconds in between two observations
    :param out_filename: name of the output CSV file
    :param max_n_obs: maximum number of observations
    :return: no return
    """

    if os.path.exists(out_filename):
        os.remove(out_filename)

    if os.path.exists(error_file):
        os.remove(error_file)

    process = None  # Initialize process for model_selection function

    for obs_count in tqdm(range(max_n_obs), desc='Monitor Progress Bar'):
        start_time = time.time()

        # Randomly decide whether to simulate a fault (the chance of fault injection is at most 20%)
        if random.random()< 0.2:
            simulate_fault()

        obs = monitor_data()
        anomaly_detected = False

        # If a possible anomaly is found, the choice of the analysis model is launched in parallel
        if obs.get('cpu_load.load_1m', 0) > 0.10:
            anomaly_detected = True
            if process is None or not process.is_alive():
                process = Process(target=model_selection, args=(csv_file, pkl_directory,))
                process.start()

        obs['analysis.possible_anomaly'] = '***' if anomaly_detected else ''
        obs['analysis.prediction_result'] = '***' if anomaly_detected else ''
        obs['analysis.used_model'] = '***' if anomaly_detected else ''

        # Writing on the command line and as a new line of a CSV file
        with open(out_filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=obs.keys())
            if obs_count == 0:
                writer.writeheader()
            writer.writerow(obs)

        # Sleeping to synchronize to the obs-interval
        exe_time_s = time.time() - start_time
        sleep_s = obs_interval_sec - exe_time_s
        # Sleep to catch up with cycle time
        if sleep_s > 0:
            time.sleep(sleep_s)
        else:
            log_error('WARNING: execution of the monitor took too long (%.3f sec)' % (exe_time_s - obs_interval_sec))
        obs_count += 1

if __name__ == "__main__":
    """
    Entry point for the Monitor
    """

    # File path
    csv_file = '../../Dataset/result_monitor.csv'
    error_file = '../../Dataset/error_log.txt'
    pkl_directory = '../../Dataset'

    # Input for monitor execution
    num_obs = 100  # maximum number of observations
    interval = 1  # Seconds in between two observations

    main_monitor(csv_file, num_obs, interval)

    #Check any errors/warnings reported in the error_log.txt file
    with open(error_file, 'r') as efile:
        lines = efile.readlines()

    error_messages = []

    for line in lines:
        start_index = line.find(' - ')
        start_index += 3

        end_index = line.find(':', start_index)

        error_message = line[start_index:end_index].strip()
        error_messages.append(error_message)

    error_counter = Counter(error_messages)
    if error_messages == []:
        print('No errors/warnings were encountered while running the Monitor.')
    else:
        print('While running the monitor you encountered the following errors/warnings:')
        for error, count in error_counter.items():
            print(f'{error} - {count}')
        print('Please check the error_log.txt file for more information.')

    delete_pkl_file(pkl_directory)