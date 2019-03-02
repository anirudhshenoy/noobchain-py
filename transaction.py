from Crypto.Hash import SHA256
import ecdsa as ec


class TxIn:
    def __init__(self, out_id, out_index):
        self.tx_out_id = out_id
        self.tx_out_index = out_index
        self.signature = None


class TxOut:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount


class Transaction:
    def __init__(self):
        self.id = None
        self.tx_ins = []
        self.tx_outs = []

    def _get_transaction_id(self):
        tx_content = ''
        for tx in self.tx_ins:
            tx_content = ''.join(
                [tx_content, tx.tx_out_id, str(tx.tx_out_index)])
        for tx in self.tx_outs:
            tx_content = ''.join([tx_content, tx.address, str(tx.amount)])
        self.id = SHA256.new(tx_content.encode('utf-8')).hexdigest()

    def push_tx_in(self, out_id, out_index):
        tx_in = TxIn(out_id, out_index)
        self.tx_ins.append(tx_in)

    def push_tx_out(self, address, amount):
        tx_out = TxOut(address, amount)
        self.tx_outs.append(tx_out)

    def sign_input_txs(self, private_key, UTXO_pool):
        for tx_in in self.tx_ins:
            if(find_utxo(UTXO_pool, tx_in)):
                signing_key = ec.SigningKey.from_string(bytes().fromhex(private_key), curve = ec.SECP256k1)
                tx_in.signature = signing_key.sign(self.id.encode('utf-8'))

class UTXO:
    def __init__(self, tx_out_id, tx_out_index, address, amount):
        self.tx_out_id = tx_out_id
        self.tx_out_index = tx_out_index
        self.address = address
        self.amount = amount


def find_UTXO(UTXO_pool, tx_in):
    for utxo in UTXO_pool:
        if (tx_in.id == utxo.tx_out_id):
            return True
    return False


if __name__ == '__main__':
    t = Transaction()
    t.push_tx_in('122213', 1231)
    t.push_tx_out('123123', 39)
    t._get_transaction_id()
    print(t.id)
