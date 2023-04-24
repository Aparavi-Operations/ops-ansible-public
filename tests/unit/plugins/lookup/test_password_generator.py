import unittest
from ansible_collections.aparavi.private.plugins.lookup.password_generator import LookupModule


class Testing(unittest.TestCase):

    gen = None

    @classmethod
    def setUpClass(cls):
      cls.gen = LookupModule()
      cls.gen._load_name = 'gen'

    def test_defaults(self):
      pwd = self.gen.run(None, None)[0]
      self.assertEqual(len(pwd), 16)

    def test_length(self):
      pwd = self.gen.run(None, None, length=4)[0]
      self.assertEqual(len(pwd), 4)

    def test_min(self):
      pwd = self.gen.run(None, None, length=6, max_special_chars=0, max_upper_chars=0, max_lower_chars=0)[0]
      assert pwd.isdigit()

if __name__ == '__main__':
    unittest.main()
