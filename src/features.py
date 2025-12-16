import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def calculate_rfm(transactions_df, snapshot_date=None):
    transactions_df = transactions_df.copy()
    transactions_df['TransactionStartTime'] = pd.to_datetime(transactions_df['TransactionStartTime'])
    if snapshot_date is None:
        snapshot_date = transactions_df['TransactionStartTime'].max() + pd.Timedelta(days=1)
    rfm_df = transactions_df.groupby('CustomerId').agg({
        'TransactionStartTime': lambda x: (snapshot_date - x.max()).days,
        'TransactionAmount': ['count', 'sum']
    })
    rfm_df.columns = ['recency', 'frequency', 'monetary']
    rfm_df.reset_index(inplace=True)
    return rfm_df

def label_high_risk(rfm_df, n_clusters=3, random_state=42):
    rfm_df = rfm_df.copy()
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_df[['recency', 'frequency', 'monetary']])
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    rfm_df['cluster'] = kmeans.fit_predict(rfm_scaled)
    cluster_summary = rfm_df.groupby('cluster')[['recency', 'frequency', 'monetary']].mean()
    high_risk_cluster = cluster_summary.sort_values(['recency', 'frequency', 'monetary'], ascending=[False, True, True]).index[0]
    rfm_df['is_high_risk'] = rfm_df['cluster'].apply(lambda x: 1 if x == high_risk_cluster else 0)
    return rfm_df
