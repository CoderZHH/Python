import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Step 1: Load the Data
matches_path = './Wimbledon_featured_matches.xlsx'
matches_data = pd.read_excel(matches_path)

# Step 2: Select Relevant Columns for Player Performance
performance_cols = ['player1', 'p1_ace', 'p1_winner', 'p1_unf_err', 'p1_break_pt_won', 'p1_distance_run',
                    'p1_net_pt_won', 'p1_break_pt_missed', 'p1_double_fault', 'p1_points_won', 'p1_sets', 'p1_games',
                    'player2', 'p2_ace', 'p2_winner', 'p2_unf_err', 'p2_break_pt_won', 'p2_distance_run',
                    'p2_net_pt_won', 'p2_break_pt_missed', 'p2_double_fault', 'p2_points_won', 'p2_sets', 'p2_games']

# Step 3: Extract and Rename Player 1 Stats
p1_stats = matches_data[['player1', 'p1_ace', 'p1_winner', 'p1_unf_err', 'p1_break_pt_won', 'p1_distance_run',
                         'p1_net_pt_won', 'p1_break_pt_missed', 'p1_double_fault', 'p1_points_won', 'p1_sets', 'p1_games']]
p1_stats.columns = ['player', 'ace', 'winner', 'unf_err', 'break_pt_won', 'distance_run',
                    'net_pt_won', 'break_pt_missed', 'double_fault', 'points_won', 'sets', 'games']

# Step 4: Extract and Rename Player 2 Stats
p2_stats = matches_data[['player2', 'p2_ace', 'p2_winner', 'p2_unf_err', 'p2_break_pt_won', 'p2_distance_run',
                         'p2_net_pt_won', 'p2_break_pt_missed', 'p2_double_fault', 'p2_points_won', 'p2_sets', 'p2_games']]
p2_stats.columns = ['player', 'ace', 'winner', 'unf_err', 'break_pt_won', 'distance_run',
                    'net_pt_won', 'break_pt_missed', 'double_fault', 'points_won', 'sets', 'games']

# Step 5: Combine Player Stats
player_stats = pd.concat([p1_stats, p2_stats], axis=0)

# Step 6: Group by Player and Calculate Mean Performance Metrics
player_grouped = player_stats.groupby('player').mean().reset_index()

# Step 7: Standardize the Data
scaler = StandardScaler()
player_features = player_grouped.drop(columns=['player'])
player_scaled = scaler.fit_transform(player_features)

# Step 8: Apply KMeans Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
player_grouped['Cluster'] = kmeans.fit_predict(player_scaled)

# Step 9: Apply PCA for Visualization
pca = PCA(n_components=2)
player_pca = pca.fit_transform(player_scaled)
player_grouped['PCA1'] = player_pca[:, 0]
player_grouped['PCA2'] = player_pca[:, 1]

# Step 10: Plot the Clusters
plt.figure(figsize=(10, 6))
for cluster in range(4):
    cluster_data = player_grouped[player_grouped['Cluster'] == cluster]
    plt.scatter(cluster_data['PCA1'], cluster_data['PCA2'], label=f'Cluster {cluster}', alpha=0.7)

plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Player Performance Clustering')
plt.legend()
plt.show()

# Step 11: Display the Clustered Players
print(player_grouped[['player', 'Cluster']])
