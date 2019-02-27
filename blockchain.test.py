import unittest
from blockchain import Blockchain


class BlockTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_block_without_genesis(self):
        chain = Blockchain()
        with self.assertRaises(IndexError):
            chain.generate_block_and_push()

    def test_genesis(self):
        chain = Blockchain()
        chain.push_genesis_block('helloworld', 2)
        chain.generate_block_and_push()
        self.assertEqual(chain.get_best_block()['height'], 2)

    def test_height(self):
        chain = Blockchain()
        chain.generate_block_and_push()
        self.assertEqual(chain.get_best_block()['height'], 3)
        previous_block = chain.get_block_from_height(2)
        self.assertEqual(chain.get_best_block()[
                         'previous_hash'], previous_block['block_hash'])

    def test_get_block_from_height(self):
        chain = Blockchain()
        self.assertFalse(chain.get_block_from_height(10000))


if __name__ == '__main__':
    unittest.main()
