"""CHF native-rate smoke tests; no external data needed."""
import unittest
import numpy as np
from benchmark import extract
from bridges import bridge_features, vector


class NativeRateTests(unittest.TestCase):
    def test_features_are_finite_at_12khz(self):
        fs=12000
        t=np.arange(2048)/fs
        x=np.sin(2*np.pi*1100*t)+0.15*np.sin(2*np.pi*2300*t)
        parts=extract(x,fs=fs)
        self.assertEqual([len(p) for p in parts],[10,3,2,4,3])
        self.assertTrue(np.isfinite(np.concatenate(parts)).all())
        self.assertTrue(900 < parts[3][2] < 1400)

    def test_bridges_are_finite_at_12khz(self):
        fs=12000
        t=np.arange(2048)/fs
        x=np.sin(2*np.pi*1000*t)+0.05*np.sin(2*np.pi*1800*t)
        b=bridge_features(x,fs=fs,max_lag=12)
        self.assertEqual(set(b),{"MS_G","G_K","K_MS"})
        self.assertEqual(len(vector(x,fs=fs)),6)
        for item in b.values():
            self.assertTrue(-12 <= item["lag_samples"] <= 12)
            self.assertTrue(-1 <= item["correlation"] <= 1)

if __name__=="__main__":
    unittest.main()
