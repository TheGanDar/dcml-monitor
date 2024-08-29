# DCML - Monitor Project
## Description
The goal of this project is to develop an anomaly detector for a specific system. The system has to be intended as a standalone system (i.e., not a distributed system) for which you have full access to resources, performance monitor from the operating system, and in which you can run custom scripts.

Your laptop is fine, tablets or other mobile devices may be fine too albeit they may raise more problems  when exercising custom scripts. The goal of this project is to develop an anomaly detector for a specific system. The system has to be intended as a standalone system (i.e., not a distributed system) for which you have full access to resources, performance monitor from the operating system, and in which you can run custom scripts

## Prerequisites
Before you begin, ensure you have met the following requirements:
+ **Python3**
+ **Pandas library**
+ **Sklearn library**
+ **Pyod library** (for import HBOS Algorithm)


## Libraries Installing 
First step is to update the "pip" package manager to the latest available version

```
python3 -m pip install --upgrade pip
```
Second step, we proceed with the installation of the main libraries for the analysis of the collected data:
+ ### Pandas library installation  
  Pandas is an Python library for data analysis and manipulation, providing powerful data structures like DataFrame (a two-dimensional table) and Series (a one-dimensional array) for handling and analyzing structured data efficiently.
  ```
  pip install pandas
  ```
+ ### Sklearn library installation
  Scikit-learn (sklearn) is an Python library for machine learning that provides simple and efficient tools for data mining and data analysis, including various algorithms for classification, regression, clustering, and dimensionality reduction.
  ```
  pip install scikit-learn numpy scipy joblib
  ```
+ ### PyOD library installation
  PyOD is an Python library for detecting anomalies in multivariate data. It provides a comprehensive suite of models for outlier detection, including classical and machine learning-based approaches, and is designed for scalability and ease of use
  ```
  pip install pyod
  ```
