import unittest
from yowsup.env import S40YowsupEnv
class S40YowsupEnvTest(unittest.TestCase):
    def test_tokengen(self):
        phone = "1234567"
        S40YowsupEnv._TOKEN_STRING  = "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1425519315543{phone}"
        env = S40YowsupEnv()
        token = env.getToken(phone)
        self.assertEqual(token, 'e84e1f1477704159efd46f6f0781dbde')
