import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

matches_path = './Wimbledon_featured_matches.xlsx'
matches_data = pd.read_excel(matches_path)

missing_values = matches_data.isnull().sum()
print("Missing Values in Each Column:")
print(missing_values)

# 检查 return_depth 缺失的行是否都是 p1_ace 或 p2_ace
missing_return_depth = matches_data[matches_data['return_depth'].isnull()]
ace_count = missing_return_depth['p1_ace'].sum() + missing_return_depth['p2_ace'].sum()
doublefault_count = missing_return_depth['p1_double_fault'].sum() + missing_return_depth['p2_double_fault'].sum()
total_missing_return_depth = missing_return_depth.shape[0]

print(f"Total missing return_depth: {total_missing_return_depth}")
print(f"Total ace in missing return_depth: {ace_count + doublefault_count}")

