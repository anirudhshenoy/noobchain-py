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

    def push_tx_in(self, out_id, out_index):
        tx_in = TxIn(out_id, out_index)
        self.tx_ins.append(tx_in)

    def push_tx_out(self, address, amount):
        tx_out = TxOut(address, amount)
        self.tx_outs.append(tx_out)

    def sign_input_txs(self, private_key, UTXO_pool=[]):
        for tx_in in self.tx_ins:
            # if(find_utxo(UTXO_pool, tx_in)):
            signing_key = ec.SigningKey.from_string(
                bytes().fromhex(private_key), curve=ec.SECP256k1)
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
            return utxo
    return False


def validate_transaction(transaction, UTXO_pool):
    tx_in_values, tx_out_values = 0
    for tx_in in transaction.tx_ins:
        utxo = find_UTXO(UTXO_pool, tx_in)
        if(type(tx_in.tx_out_id) != str and
           type(tx_in.tx_out_index) != int and
           type(tx_in.signature) != str and
           utxo):
            return False
        tx_in_values += utxo.amount
    for tx_out in transaction.tx_outs:
        if(type(tx_out.address) != str and
           type(tx_out.amount) != int):
            return False
        tx_out_values += tx_out.amount
    if(get_transaction_id(transaction) != transaction.id):
        return False
    if(tx_out_values != tx_in_values):
        return False
    return True


def validate_coinbase_transaction(transaction, block_height):
    if(len(transaction.tx_ins) != 1):
        return False
    if(get_transaction_id(transaction != transaction.id)):
        return False
    if(transaction.tx_ins[0].tx_out_index != block_height):
        return False
    return True


def get_transaction_id(transaction):
    tx_content = ''
    for tx in transaction.tx_ins:
        tx_content = ''.join(
            [tx_content, tx.tx_out_id, str(tx.tx_out_index)])
    for tx in transaction.tx_outs:
        tx_content = ''.join([tx_content, tx.address, str(tx.amount)])
    return SHA256.new(tx_content.encode('utf-8')).hexdigest()


def generate_coinbase_transaction(self, block_height, address):
    _COINBASE_AMOUNT = 50
    coinbase_tx = Transaction()
    coinbase_tx.push_tx_in('', block_height)
    coinbase_tx.push_tx_out(address, _COINBASE_AMOUNT)
    return coinbase_tx


if __name__ == '__main__':
    t = Transaction()
    t.push_tx_in('122213', 1231)
    t.push_tx_out('123123', 39)
    t.id = get_transaction_id(t)
    print(t.id)
    private_key = ec.SigningKey.generate(curve=ec.SECP256k1).to_string().hex()
    t.sign_input_txs(private_key)
    print(t.tx_ins[0].signature.hex())
