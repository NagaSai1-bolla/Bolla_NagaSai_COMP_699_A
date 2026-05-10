import unittest
from models.ml_engine import WaitingTimeMLEngine


class TestBlackBoxML(unittest.TestCase):

    def test_case_1(self):
        result = WaitingTimeMLEngine.predict_wait(5, 10)
        self.assertEqual(result, 50)

    def test_case_2(self):
        result = WaitingTimeMLEngine.predict_wait(3, 4)
        self.assertEqual(result, 12)

    def test_case_3(self):
        result = WaitingTimeMLEngine.predict_wait(1, 2)
        self.assertEqual(result, 2)

    def test_case_4(self):
        result = WaitingTimeMLEngine.predict_wait(8, 6)
        self.assertEqual(result, 48)

    def test_case_5(self):
        result = WaitingTimeMLEngine.predict_wait(0, 5)
        self.assertEqual(result, 0)

    def test_case_6(self):
        result = WaitingTimeMLEngine.predict_wait(6, 0)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()