import unittest
from block import Block
from blockchain import Blockchain


class BlockTest(unittest.TestCase):
    def CreateChain(self):
        chain = Blockchain()
        block = Block()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
