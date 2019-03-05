import unittest
import transaction as tx
import ecdsa as ec


class TransactionTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_transaction(self):
        t = tx.Transaction()
        t.push_tx_in('111111', 10)
        t.push_tx_out('222222', 39)
        t.id = tx.get_transaction_id(t)
        self.assertEqual(t.get_json()['vin'][0]['tx_out_id'], '111111')
        self.assertEqual(t.get_json()['vin'][0]['tx_out_index'], 10)
        self.assertEqual(t.get_json()['vout'][0]['address'], '222222')
        self.assertEqual(t.get_json()['vout'][0]['amount'], 39)

    def test_create_coinbase(self):
        block_height = 1
        address = 'address2233321'
        t = tx.generate_coinbase_transaction(block_height, address)
        t.id = tx.get_transaction_id(t)
        self.assertEqual(t.get_json()['vin'][0]['tx_out_id'], '')
        self.assertEqual(t.get_json()['vin'][0]['tx_out_index'], block_height)
        self.assertEqual(t.get_json()['vout'][0]['address'], address)
        self.assertEqual(t.get_json()['vout'][0]['amount'], 50)

    def test_validate_coinbase(self):
        block_height = 1
        address = 'address2233321'
        t = tx.generate_coinbase_transaction(block_height, address)
        t.id = tx.get_transaction_id(t)
        self.assertTrue(tx.validate_coinbase_transaction(t, block_height))

    def test_validate_coinbase_multiple_input(self):
        block_height = 1
        address = 'address2233321'
        t = tx.generate_coinbase_transaction(block_height, address)
        t.push_tx_in('11111', 10)
        t.id = tx.get_transaction_id(t)
        self.assertFalse(tx.validate_coinbase_transaction(t, block_height))

    def test_transaction_hash(self):
        t = tx.Transaction()
        t.push_tx_in('111111', 10)
        t.push_tx_out('222222', 39)
        t.id = tx.get_transaction_id(t)
        t.id = 'f6a323f34c9605a8995ef20db584a462d93db5132abf14ccb18b3528644df921'
        self.assertEqual(t.id, tx.get_transaction_id(t))

    def test_transaction_signature(self):
        private_key = ec.SigningKey.generate(
            curve=ec.SECP256k1).to_string().hex()
        signing_key = ec.SigningKey.from_string(
            bytes().fromhex(private_key), curve=ec.SECP256k1)
        t = tx.Transaction()
        t.push_tx_in('111111', 10)
        t.push_tx_out('222222', 39)
        t.id = tx.get_transaction_id(t)
        u = tx.UTXO('111111', 0, '22', 39)
        t.sign_input_txs(private_key, [u])
        signature = signing_key.sign(t.id.encode('utf-8')).hex()
        verifying_key = signing_key.get_verifying_key()
        assert verifying_key.verify(
            bytes().fromhex(signature), t.id.encode('utf-8'))

    def test_validate_transaction(self):
        t = tx.Transaction()
        t.push_tx_in('111111', 10)
        t.push_tx_out('222222', 39)
        t.id = tx.get_transaction_id(t)
        u = tx.UTXO('111111', 0, '22', 39)
        self.assertTrue(tx.validate_transaction(t, [u]))

    def test_validate_transaction_incorrect_in_out_amount(self):
        t = tx.Transaction()
        t.push_tx_in('111111', 10)
        t.push_tx_out('222222', 39)
        t.id = tx.get_transaction_id(t)
        u = tx.UTXO('111111', 0, '22', 10)
        self.assertFalse(tx.validate_transaction(t, [u]))

    def test_validate_transaction_incorrect_structure(self):
        t = tx.Transaction()
        t.push_tx_in('111111', '10')
        t.push_tx_out('222222', 39)
        t.id = tx.get_transaction_id(t)
        u = tx.UTXO('111111', 0, '22', 10)
        self.assertFalse(tx.validate_transaction(t, [u]))


if __name__ == '__main__':
    unittest.main()
