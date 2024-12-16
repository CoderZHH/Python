import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Step 1: Load the Data
matches_path = './Wimbledon_featured_matches.xlsx'
matches_data = pd.read_excel(matches_path)

# Step 2: Select Relevant Columns for Round Performance
round_cols = ['set_no', 'game_no', 'point_no', 'rally_count', 'speed_mph',
              'p1_distance_run', 'p2_distance_run', 'p1_ace', 'p2_ace',
              'p1_winner', 'p2_winner', 'p1_unf_err', 'p2_unf_err',
              'p1_break_pt', 'p2_break_pt']

round_stats = matches_data[round_cols].copy()

# Step 3: Check for Missing Values Before Imputation
missing_values = round_stats.isnull().sum()
print("Missing Values in Each Column:")
print(missing_values)

# Step 4: Create Combined and Derived Metrics for Each Round
round_stats['total_distance_run'] = round_stats['p1_distance_run'] + round_stats['p2_distance_run']
round_stats['total_ace'] = round_stats['p1_ace'] + round_stats['p2_ace']
round_stats['total_winner'] = round_stats['p1_winner'] + round_stats['p2_winner']
round_stats['total_unf_err'] = round_stats['p1_unf_err'] + round_stats['p2_unf_err']
round_stats['total_break_pt'] = round_stats['p1_break_pt'] + round_stats['p2_break_pt']
round_stats['distance_ratio'] = round_stats['p1_distance_run'] / (round_stats['p2_distance_run'] + 1e-5)
round_stats['winner_ratio'] = round_stats['p1_winner'] / (round_stats['p2_winner'] + 1e-5)
round_stats['ace_ratio'] = round_stats['p1_ace'] / (round_stats['p2_ace'] + 1e-5)
round_stats['unf_err_ratio'] = round_stats['p1_unf_err'] / (round_stats['p2_unf_err'] + 1e-5)

# Drop individual player columns to focus on round-level and derived metrics
round_features = round_stats[['rally_count', 'speed_mph', 'total_distance_run',
                              'total_ace', 'total_winner', 'total_unf_err', 'total_break_pt',
                              'distance_ratio', 'winner_ratio', 'ace_ratio', 'unf_err_ratio']]

# Step 5: Check for Missing Values in New Features
missing_values_combined = round_features.isnull().sum()
print("Missing Values in Derived Features:")
print(missing_values_combined)

# Step 6: Stop Before Imputation
print("Stopping before imputing missing values. Data needs further analysis.")
