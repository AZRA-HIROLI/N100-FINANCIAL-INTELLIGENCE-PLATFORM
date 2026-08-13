import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_kmeans_clustering(df_features: pd.DataFrame) -> tuple:
    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct"
    ]

    df_proc = df_features[["company_id", "sector"] + features].copy()

    # Impute missing values with sector median
    for feat in features:
        df_proc[feat] = df_proc.groupby("sector")[feat].transform(lambda x: x.fillna(x.median()))
        df_proc[feat] = df_proc[feat].fillna(df_proc[feat].median())

    X = df_proc[features].values

    # Standard scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Generate Elbow Plot (k from 2 to 10)
    inertias = []
    k_range = range(2, 11)
    for k in k_range:
        km_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
        km_temp.fit(X_scaled)
        inertias.append(km_temp.inertia_)

    plt.figure(figsize=(8, 4.5))
    plt.plot(k_range, inertias, 'bo-', linewidth=2, markersize=7)
    plt.axvline(x=5, color='r', linestyle='--', label='Selected k=5')
    plt.title('KMeans Elbow Method (Inertia vs k)', fontsize=12, fontweight='bold')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia (WCSS)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("reports/elbow_plot.png", dpi=300)
    plt.close()

    # Fit KMeans with k=5
    kmeans_5 = KMeans(n_clusters=5, random_state=42, n_init=10)
    cluster_ids = kmeans_5.fit_predict(X_scaled)
    centroids = kmeans_5.cluster_centers_

    # Calculate distance from assigned centroid
    distances = []
    for i, cid in enumerate(cluster_ids):
        dist = np.linalg.norm(X_scaled[i] - centroids[cid])
        distances.append(round(float(dist), 4))

    default_names = {
        0: "Cluster 0 - High Quality",
        1: "Cluster 1 - Moderate Growth",
        2: "Cluster 2 - Capital Intensive",
        3: "Cluster 3 - High Leverage",
        4: "Cluster 4 - Emerging"
    }

    df_proc["cluster_id"] = cluster_ids
    df_proc["cluster_name"] = df_proc["cluster_id"].map(default_names)
    df_proc["distance_from_centroid"] = distances

    df_output = df_proc[["company_id", "cluster_id", "cluster_name", "distance_from_centroid"]]
    return df_output, df_proc, scaler, kmeans_5
