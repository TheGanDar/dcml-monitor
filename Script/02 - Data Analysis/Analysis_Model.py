# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario
# A.A: 2023/2024

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from pyod.models.hbos import HBOS
from sklearn.decomposition import PCA

os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # Sostituisci '4' con il numero di core che vuoi usare (per la libreria joblib, serve anche pers cikit-learn perchè usa joblib)

# Caricamento del dataset
csv_file = '../../Dataset/result_monitor.csv'
data = pd.read_csv(csv_file)

# Preparazione dei dati
data = data.dropna()

# Seleziona le caratteristiche per X
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

# Genera manualmente `y` se non esiste una colonna nel dataset
# Esempio di creazione di una colonna y basata su una condizione
y = (data['cpu_load.load_1m'] > 1.5).astype(int)  # Condizione d'esempio, da adattare alle tue esigenze

# Suddivisione dei dati in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=35)

num_components = min(X_train.shape[1], X_train.shape[0] - 1)
pca = PCA(n_components=num_components)

# Riduzione dimensionale con PCA
#pca = PCA(n_components=X_train.shape[1] - 1)  # Riduci di una dimensione per evitare la non invertibilità
X_train_reduced = pca.fit_transform(X_train)
X_test_reduced = pca.transform(X_test)


# Standardizzazione delle caratteristiche
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_reduced)
X_test = scaler.transform(X_test_reduced)

# Definizione dei modelli

# 1. DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)

# 2. Modello HBOS
hbos = HBOS(contamination=0.1)

# 3. K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)  # Sostituisci n_neighbors con il valore che preferisci


# Training e predizione con DBSCAN
dbscan.fit(X_train)
dbscan_labels = dbscan.fit_predict(X_test)

# Training e predizione con il modello statistico utilizzando l'algoritmo HBOS
hbos.fit(X_train)
hbos_labels = hbos.predict(X_test)

# Training e predizione con KNN
knn.fit(X_train, y_train)
knn_labels = knn.predict(X_test)

# Normalizzazione delle etichette per confronto (DBSCAN etichetta gli outliers come -1)
dbscan_labels = np.where(dbscan_labels == -1, 1, 0)
hbos_labels = np.where(hbos_labels == 1, 1, 0)

# Calcolo delle metriche
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

# Scelta del miglior modello basato su F1-score
best_model_name = max(models_performance, key=lambda x: models_performance[x]['f1'])
print(f"Il miglior modello è: {best_model_name} con F1-score: {models_performance[best_model_name]['f1']}")

# Salvataggio del modello migliore
if best_model_name == 'DBSCAN':
    best_model = dbscan
elif best_model_name == 'Statistical Model':
    best_model = hbos
else:
    best_model = knn

for model_name, metrics in models_performance.items():
    print(f"F1-score del modello {model_name}: {metrics['f1']:.10f}")

# Salvataggio del modello migliore

pkl_directory = '../../Dataset'  # Sostituisci con il percorso della tua directory

model_filename = f'{pkl_directory}/{best_model_name.replace(" ", "_")}_best_model.pkl'
joblib.dump(best_model, model_filename)
print(f"Modello salvato come: {model_filename}")



# Elenca tutti i file nella directory con estensione .pkl
files_to_delete = [f for f in os.listdir(pkl_directory) if f.endswith('.pkl')]
if files_to_delete:
     for file_name in files_to_delete:
        file_path = os.path.join(pkl_directory, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Errore nell'eliminazione di {file_path}: {e}")