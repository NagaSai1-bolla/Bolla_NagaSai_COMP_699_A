import unittest
from models.ml_engine import WaitingTimeMLEngine


class TestWhiteBoxML(unittest.TestCase):

    def test_valid_values(self):
        result = WaitingTimeMLEngine.predict_wait(5, 10)
        self.assertTrue(result > 0)

    def test_zero_queue(self):
        result = WaitingTimeMLEngine.predict_wait(0, 10)
        self.assertEqual(result, 0)

    def test_negative_queue(self):
        result = WaitingTimeMLEngine.predict_wait(-1, 10)
        self.assertEqual(result, 0)

    def test_zero_service_time(self):
        result = WaitingTimeMLEngine.predict_wait(5, 0)
        self.assertEqual(result, 0)

    def test_large_values(self):
        result = WaitingTimeMLEngine.predict_wait(10, 5)
        self.assertTrue(result > 0)

    def test_small_values(self):
        result = WaitingTimeMLEngine.predict_wait(2, 3)
        self.assertTrue(result > 0)


if __name__ == "__main__":
    unittest.main()