import unittest
from blockchain import Blockchain
from pprint import pprint


class BlockTest(unittest.TestCase):
    chain = Blockchain()

    def setUp(self):
        pass

    def test_a_create_block_without_genesis(self):
        with self.assertRaises(IndexError):
            self.chain.generate_block_and_push()

    def test_b_genesis(self):
        self.chain.push_genesis_block('helloworld', 2)
        self.chain.generate_block_and_push()
        self.assertEqual(self.chain.get_best_block()['height'], 2)

    def test_c_height(self):
        self.chain.generate_block_and_push()
        self.assertEqual(self.chain.get_best_block()['height'], 3)
        previous_block = self.chain.get_block_from_height(2)
        self.assertEqual(self.chain.get_best_block()[
                         'previous_hash'], previous_block['block_hash'])

    def test_d_get_block_from_height(self):
        self.assertFalse(self.chain.get_block_from_height(10000))

    def test_e_get_chain_length(self):
        self.assertEqual(len(self.chain), 3)

    def test_f_get_chain_difficulty(self):
        print(len(self.chain))
        self.assertEqual(self.chain.get_cummulative_difficulty(), 12)

if __name__ == '__main__':
    unittest.main()
