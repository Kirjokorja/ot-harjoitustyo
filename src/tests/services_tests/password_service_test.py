import unittest
from bcrypt import checkpw
from services.password_service import PasswordService


class TestPasswordService(unittest.TestCase):
    def setUp(self):
        self.pw_service = PasswordService(5)
        self.pw = "Moikka!"
        self.hashed_pw = self.pw_service.hash_password(self.pw)
        self.hashed_pw_bytes = self.hashed_pw.encode('utf-8')
        self.pw_bytes = self.pw.encode('utf-8')

    def test_password_service_gets_correct_min_pw_lenght(self):
        self.assertEqual(self.pw_service.get_min_password_lenght(), 5)

    def test_hash_password_returns_a_string(self):
        self.assertEqual(type(self.hashed_pw), type(str()))

    def test_hash_password_returns_a_hashed_string(self):
        hashed_pw_bytes = self.hashed_pw.encode('utf-8')
        pw_bytes = self.pw.encode('utf-8')
        self.assertTrue(checkpw(pw_bytes, hashed_pw_bytes))

    def test_password_match_returns_true_if_match(self):
        self.assertTrue(self.pw_service.password_match(
            self.hashed_pw, self.pw))

    def test_password_match_returns_false_if_not_match(self):
        wrong_pw = "Moro!"
        self.assertFalse(self.pw_service.password_match(
            self.hashed_pw, wrong_pw))

    def test_password_long_enough_returns_true_if_as_long_as_min_lenght(self):
        min_lenght_pw = "viisi"
        self.assertTrue(self.pw_service.password_long_enough(min_lenght_pw))

    def test_password_long_enough_returns_true_if_longer_than_min_lenght(self):
        self.assertTrue(self.pw_service.password_long_enough(self.pw))

    def test_password_long_enough_returns_false_if_shorter_than_min_lenght(self):
        short_pw = "v"
        self.assertFalse(self.pw_service.password_long_enough(short_pw))
