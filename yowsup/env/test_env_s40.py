import unittest
from yowsup.env import S40YowsupEnv
class S40YowsupEnvTest(unittest.TestCase):
    def test_tokengen(self):
        phone = "1234567"
        S40YowsupEnv._TOKEN_STRING  = "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1418865329241{phone}"
        env = S40YowsupEnv()
        token = env.getToken(phone)
        self.assertEqual(token, '71780696500214e7c14433dc6e0eefdb')
