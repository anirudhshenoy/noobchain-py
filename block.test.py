import unittest
from block import Block


class BlockTest(unittest.TestCase):
    def setUp(self):
        self.block = Block()

    def test(self):
        print(str(self.block))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
