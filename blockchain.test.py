import unittest
from block import Block
from blockchain import Blockchain


class BlockTest(unittest.TestCase):
    def CreateChain(self):
        chain = Blockchain()
        chain.push_genesis_block('helloworld', 2)
        print(chain.chain)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
