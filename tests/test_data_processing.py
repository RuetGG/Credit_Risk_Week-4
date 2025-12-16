import unittest
import pandas as pd
from src.features import calculate_rfm, label_high_risk

class TestFeatureEngineering(unittest.TestCase):

    def setUp(self):
        data = {
            'CustomerId': ['C1', 'C1', 'C2', 'C2', 'C3'],
            'TransactionStartTime': [
                '2025-12-01', '2025-12-05',
                '2025-12-03', '2025-12-04',
                '2025-12-02'
            ],
            'TransactionAmount': [100, 200, 50, 50, 300]
        }
        self.transactions = pd.DataFrame(data)

    def test_calculate_rfm(self):
        rfm = calculate_rfm(self.transactions, snapshot_date=pd.Timestamp('2025-12-10'))
        self.assertIn('recency', rfm.columns)
        self.assertIn('frequency', rfm.columns)
        self.assertIn('monetary', rfm.columns)
        self.assertEqual(len(rfm), 3)

    def test_label_high_risk(self):
        rfm = calculate_rfm(self.transactions, snapshot_date=pd.Timestamp('2025-12-10'))
        rfm_labeled = label_high_risk(rfm, n_clusters=2, random_state=42)
        self.assertIn('is_high_risk', rfm_labeled.columns)
        self.assertTrue(set(rfm_labeled['is_high_risk']).issubset({0, 1}))
        self.assertEqual(len(rfm_labeled), 3)

if __name__ == '__main__':
    unittest.main()