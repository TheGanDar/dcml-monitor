# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario Gangemi
# Student ID: 7062188
# A.A: 2023/2024

import os
import csv
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from pyod.models.hbos import HBOS

def delete_pkl_file(pkl_directory):
    """
    Function to delete all files in the 'Dataset' directory with .pkl exstension.
    :param pkl_directory: directory that contains .pkl files
    """
    files_to_delete = [f for f in os.listdir(pkl_directory) if f.endswith('.pkl')]
    if files_to_delete:
        for file_name in files_to_delete:
            file_path = os.path.join(pkl_directory, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def model_selection(path_csv_file, path_pkl_directory):
    """
    Function to choose the best model for predicting a possible anomaly.
    :param pkl_directory: directory that contains .pkl files
    :param path_csv_file: directory that contains result_monitor.csv file
    """

    os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # Sostituisci '4' con il numero di core che vuoi usare (per la libreria joblib, serve anche pers cikit-learn perchè usa joblib)

    delete_pkl_file(path_pkl_directory)

    # uploading and managing the dataset
    data = pd.read_csv(path_csv_file)
    data = data.dropna()

    X = data[['cpu_times.user', 'cpu_times.system', 'cpu_times.idle', 'cpu_times.interrupt',
              'cpu_times.dpc', 'cpu_stats.ctx_switches', 'cpu_stats.interrupts',
              'cpu_stats.soft_interrupts', 'cpu_stats.syscalls', 'cpu_load.load_1m',
              'cpu_load.load_5m', 'cpu_load.load_15m', 'swap.total', 'swap.used',
              'swap.free', 'swap.percent', 'swap.sin', 'swap.sout', 'virtual.total',
              'virtual.available', 'virtual.percent', 'virtual.used', 'virtual.free',
              'disk.total', 'disk.used', 'disk.free', 'disk.percent', 'disk_io.read_count',
              'disk_io.write_count', 'disk_io.read_bytes', 'disk_io.write_bytes',
              'disk_io.read_time', 'disk_io.write_time', 'net_io.bytes_sent',
              'net_io.bytes_recv', 'net_io.packets_sent', 'net_io.packets_recv',
              'net_io.errin', 'net_io.errout', 'net_io.dropin', 'net_io.dropout']]

    y = (data['cpu_load.load_1m'] > 0.07).astype(int) # It generates a vector named 'y' when the selected column is greater than 0.07 (used for create the y_train and y_test variables)

    # Dataset splitting between training and test
    if len(X) > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=35)
    else:
        X_train, X_test, y_train, y_test = X, X, y, y

    #Standardization
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Definition of the models

    # 1. DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=5)

    # 2. HBOS
    hbos = HBOS(contamination=0.1)

    # 3. K-Nearest Neighbors (KNN)
    knn = KNeighborsClassifier(n_neighbors=min(5, len(X_train)))

    # Training and prediction with the different models
    dbscan.fit(X_train)
    dbscan_labels = dbscan.fit_predict(X_test)

    hbos.fit(X_train)
    hbos_labels = hbos.predict(X_test)

    knn.fit(X_train, y_train)
    knn_labels = knn.predict(X_test)

    # Normalization for DBSCAN and HBOS models for comparing them
    dbscan_labels = np.where(dbscan_labels == -1, 1, 0)
    hbos_labels = np.where(hbos_labels == 1, 1, 0)

    # Metrics calculation Accuracy, Precision, Recall and F1-score
    models_performance = {
        'DBSCAN': {
            'accuracy': accuracy_score(y_test, dbscan_labels),
            'precision': precision_score(y_test, dbscan_labels, zero_division=0),
            'recall': recall_score(y_test, dbscan_labels, zero_division=0),
            'f1': f1_score(y_test, dbscan_labels, zero_division=0)
        },
        'HBOS': {
            'accuracy': accuracy_score(y_test, hbos_labels),
            'precision': precision_score(y_test, hbos_labels, zero_division=0),
            'recall': recall_score(y_test, hbos_labels, zero_division=0),
            'f1': f1_score(y_test, hbos_labels, zero_division=0)
        },
        'KNN': {
            'accuracy': accuracy_score(y_test, knn_labels),
            'precision': precision_score(y_test, knn_labels, zero_division=0),
            'recall': recall_score(y_test, knn_labels, zero_division=0),
            'f1': f1_score(y_test, knn_labels, zero_division=0)
        }
    }

    # Choose and save the best model based on F1-score
    best_model_name = max(models_performance, key=lambda x: models_performance[x]['f1'])
    if best_model_name == 'DBSCAN':
        best_model = dbscan
    elif best_model_name == 'Statistical Model':
        best_model = hbos
    else:
        best_model = knn
    model_filename = f'{path_pkl_directory}/{best_model_name.replace(" ", "_")}_best_model.pkl'
    joblib.dump(best_model, model_filename)

    anomaly_detection_prediction(path_csv_file, path_pkl_directory)

def anomaly_detection_prediction(path_csv_file, path_pkl_directory):
    """
    Function that load the saved model and uses it to predict anomalies.

    :param pkl_directory: directory that contains .pkl files
    :param path_csv_file: directory that contains result_monitor.csv file
    """

    model_filenames = [f for f in os.listdir(path_pkl_directory) if f.endswith('_best_model.pkl')]
    if not model_filenames:
        raise FileNotFoundError("There is any saved model in the specified directory.")

    # Load best model and dataset
    best_model_filename = os.path.join(path_pkl_directory, model_filenames[0])
    best_model = joblib.load(best_model_filename)
    data = pd.read_csv(path_csv_file)

    # Filtering the rows where the possible_anomaly and prediction_result are equals to '***'
    data_anomalies = data[(data['analysis.possible_anomaly'] == '***') & (data['analysis.prediction_result'] == '***')]

    # Iterating on the filtered rows
    for index, row in data_anomalies.iterrows():
        X = row[['cpu_times.user', 'cpu_times.system', 'cpu_times.idle', 'cpu_times.interrupt',
                 'cpu_times.dpc', 'cpu_stats.ctx_switches', 'cpu_stats.interrupts',
                 'cpu_stats.soft_interrupts', 'cpu_stats.syscalls', 'cpu_load.load_1m',
                 'cpu_load.load_5m', 'cpu_load.load_15m', 'swap.total', 'swap.used',
                 'swap.free', 'swap.percent', 'swap.sin', 'swap.sout', 'virtual.total',
                 'virtual.available', 'virtual.percent', 'virtual.used', 'virtual.free',
                 'disk.total', 'disk.used', 'disk.free', 'disk.percent', 'disk_io.read_count',
                 'disk_io.write_count', 'disk_io.read_bytes', 'disk_io.write_bytes',
                 'disk_io.read_time', 'disk_io.write_time', 'net_io.bytes_sent',
                 'net_io.bytes_recv', 'net_io.packets_sent', 'net_io.packets_recv',
                 'net_io.errin', 'net_io.errout', 'net_io.dropin', 'net_io.dropout']].values.reshape(1, -1)

        # Standardization
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Prediction
        if isinstance(best_model, DBSCAN):
            prediction = best_model.fit_predict(X_scaled)
            anomaly_confirmed = prediction[0] == -1
        else:
            prediction = best_model.predict(X_scaled)
            anomaly_confirmed = prediction[0] == 1

        # The result of the prediction is written in 'prediction_result' column and the used model is written in 'used_model' column
        with open(path_csv_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        col_index_prediction = rows[0].index('analysis.prediction_result')
        col_index_model = rows[0].index('analysis.used_model')

        rows[index + 1][col_index_prediction] = 'Anomaly!' if anomaly_confirmed else 'Fake Anomaly'

        with open(path_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        rows[index + 1][col_index_model] = best_model

        with open(path_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)