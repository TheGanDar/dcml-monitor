# DATA COLLECTION AND MACHINE LEARNING
# FOR CRITICAL CYBER-PHYSICAL SYSTEMS project
# Name: Dario
# A.A: 2023/2024

import pandas as pd



# Reading a CSV file into a DataFrame pandas object
source_ds = pd.read_csv("../../Dataset/result_monitor.csv", sep=',')
result_ds = pd.DataFrame(source_ds)

print(result_ds)
