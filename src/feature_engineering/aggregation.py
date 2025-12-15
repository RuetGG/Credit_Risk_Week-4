from sklearn.base import BaseEstimator, TransformerMixin

class Aggregator(BaseEstimator, TransformerMixin):
    def __init__(self, customer_col='CustomerId', amount_col='Amount'):
        self.customer_col = customer_col
        self.amount_col = amount_col
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        numeric_agg = (
            X.groupby(self.customer_col)[self.amount_col]
            .agg(
                total_transaction_amount = "sum",
                avg_transaction_amount = "mean",
                transaction_count = "count",
                std_transaction_amount = "std"
            )
            .reset_index()
        )
        cat_agg = X.groupby(self.customer_col).agg(
            product = ("ProductCategory", lambda x: x.mode().iloc[0]),
            provider = ("ProviderId", lambda x: x.mode().iloc[0]),
            channel = ("ChannelId", lambda x: x.mode().iloc[0]),
        ).reset_index()
        
        merge =  numeric_agg.merge(cat_agg, on='CustomerId', how='left')

        return merge