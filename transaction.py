from Crypto.Hash import SHA256
import ecdsa as ec
import json
import pprint


class TxIn:
    def __init__(self, out_id, out_index):
        self.tx_out_id = out_id
        self.tx_out_index = out_index
        self.signature = None

    def get_json(self):
        tx_in_object = {
            'tx_out_id': self.tx_out_id,
            'tx_out_index': self.tx_out_index,
            'signature': self.signature
        }
        return tx_in_object


class TxOut:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def get_json(self):
        tx_out_object = {
            'address': self.address,
            'amount': self.amount
        }
        return tx_out_object


class Transaction:
    def __init__(self):
        self.tx_ins = []
        self.tx_outs = []
        self.id = None

    def get_json(self):
        vin = []
        vout = []
        for tx_in in self.tx_ins:
            vin.append(tx_in.get_json())
        for tx_out in self.tx_outs:
            vout.append(tx_out.get_json())
        transaction_json = {
            'id': self.id,
            'vin': vin,
            'vout': vout
        }
        return transaction_json

    def generate_tx_hash(self):
        self.id = get_transaction_id(self)

    def __str__(self):
        return json.dumps(self.get_json())

    def push_tx_in(self, out_id, out_index):
        tx_in = TxIn(out_id, out_index)
        self.tx_ins.append(tx_in)

    def push_tx_out(self, address, amount):
        tx_out = TxOut(address, amount)
        self.tx_outs.append(tx_out)

    def sign_input_txs(self, private_key, UTXO_pool=[]):
        for tx_in in self.tx_ins:
            if(find_UTXO(UTXO_pool, tx_in)):
                signing_key = ec.SigningKey.from_string(
                    bytes().fromhex(private_key), curve=ec.SECP256k1)
                tx_in.signature = signing_key.sign(
                    self.id.encode('utf-8')).hex()


class UTXO:
    def __init__(self, tx_id, tx_out_index, address, amount):
        self.tx_id = tx_id
        self.tx_out_index = tx_out_index
        self.address = address
        self.amount = amount

    def get_json(self):
        json_object = {
            'tx_id': self.tx_id,
            'tx_out_index': self.tx_out_index,
            'address': self.address,
            'amount': self.amount
        }
        return json_object


def find_UTXO(UTXO_pool, tx_in):
    for utxo in UTXO_pool:
        if (tx_in.tx_out_id == utxo.tx_id):
            return utxo
    return False


def verify_signature(signature, public_key, tx_id):
    verifying_key = ec.VerifyingKey.from_string(
        bytes().fromhex(public_key), curve=ec.SECP256k1)
    try:
        check = verifying_key.verify(
            bytes().fromhex(signature), tx_id.encode('utf-8'))
    except:
        check = False
    finally:
        return check


def validate_transaction(transaction, UTXO_pool):
    tx_in_values = 0
    tx_out_values = 0
    for tx_in in transaction.tx_ins:
        utxo = find_UTXO(UTXO_pool, tx_in)
        if(type(tx_in.tx_out_id) != str and
           type(tx_in.tx_out_index) != int and
           type(tx_in.signature) != str and
           utxo):
            return False
        if(not verify_signature(tx_in.signature, utxo.address, transaction.id)):
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
    if(get_transaction_id(transaction) != transaction.id):
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


def generate_coinbase_transaction(block_height, address):
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
    print(t.tx_ins[0].signature)
    print(str(t))
