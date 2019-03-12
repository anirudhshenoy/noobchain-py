from Crypto.Hash import SHA256
import ecdsa as ec
import json


class TxIn:
    """
    Class: Input Transaction
    tx_out_id(str) : Tx Id hash that is being referenced
    tx_out_index(int) : Index of tx out being referenced
    signature(str) : Signature to unlock UTXO
    """

    def __init__(self, out_id, out_index):
        self.tx_out_id = out_id
        self.tx_out_index = out_index
        self.signature = None

    def get_json(self):
        """
        Return JSON object (dict) of tx_in
        """
        tx_in_object = {
            'tx_out_id': self.tx_out_id,
            'tx_out_index': self.tx_out_index,
            'signature': self.signature
        }
        return tx_in_object


class TxOut:
    """
    Class: Output transaction
    address(str) : Public key (verifying key) to send transaction to
    amount(int) : Amount of coins to send
    """

    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def get_json(self):
        """
        Returns JSON object(dict) of tx_out
        """
        tx_out_object = {
            'address': self.address,
            'amount': self.amount
        }
        return tx_out_object


class Transaction:
    """
    Class : Tranasction
    id(str) : SHA256 hash of the transaction
    tx_ins(list) : List of tx_in instances
    tx_outs(list) : List of tx_out instances
    """

    def __init__(self):
        self.tx_ins = []
        self.tx_outs = []
        self.id = None

    def get_json(self):
        """
        Get JSON (dict) of transaction
        """
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
        """
        Generate hash for the transaction and set it to id
        """
        self.id = get_transaction_id(self)

    def __str__(self):
        return json.dumps(self.get_json())

    def push_tx_in(self, out_id, out_index):
        """
        Add an input transaction to tx_ins
        """
        tx_in = TxIn(out_id, out_index)
        self.tx_ins.append(tx_in)

    def push_tx_out(self, address, amount):
        """
        Add an output transaction to tx_outs
        """
        tx_out = TxOut(address, amount)
        self.tx_outs.append(tx_out)

    def sign_input_txs(self, private_key, UTXO_pool=[]):
        """
        Sign all input transactions

        Arguments:
        private_key(str): private key in hex format to sign inputs
        UTXO_pool(list): list of UTXO instances
        """
        # Create a signing key object from the private key
        signing_key = ec.SigningKey.from_string(
            bytes().fromhex(private_key), curve=ec.SECP256k1)
        for tx_in in self.tx_ins:
            if(find_UTXO(UTXO_pool, tx_in)):
                tx_in.signature = signing_key.sign(
                    self.id.encode('utf-8')).hex()


class UTXO:
    """
    Class: Unspent Transaction Output

    tx_id(str) : Transaction hash(id) of the transaction being referenced
    tx_out_index(int) : index # of output in the transaction
    address(str) : Address that the UTXO belongs to
    amount(int) : Amount of the UTXO
    """

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
    """
    Check if UTXO exists in the pool

    Args:
    UTXO_pool(list) : list of all UTXO instances currently available
    tx_in(Tx_in) : transaction input instance

    Returns:
    UTXO instance if it exists, false if not
    """
    for utxo in UTXO_pool:
        if (tx_in.tx_out_id == utxo.tx_id):
            return utxo
    return False


def verify_signature(signature, public_key, tx_id):
    """
    Verify that the signature is correct

    Arguments:
    signature(str) : signature of the tx_in
    public_key(str) : public key/address in hex format
    tx_id(str) : transaction hash/id of the transaction being referenced

    Returns:
    Boolean: True if signature is correct
    """
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
    """
    Validates the transaction

    Arguments:
    transaction(Transaction): instance of the transaction to be validated
    UTXO_pool(list) : list of UTXO instances

    Returns:
    Boolean : True if transaction is valid
    """
    tx_in_values = 0
    tx_out_values = 0
    for tx_in in transaction.tx_ins:
        utxo = find_UTXO(UTXO_pool, tx_in)
        if(not utxo):           # If UTXO doesn't exist return False
            return False
        if(type(tx_in.tx_out_id) != str or    # Check transaction structure
           type(tx_in.tx_out_index) != int or
           type(tx_in.signature) != str):
            return False
        # Check signatures
        if(not verify_signature(tx_in.signature, utxo.address, transaction.id)):
            return False
        tx_in_values += utxo.amount
    for tx_out in transaction.tx_outs:
        if(type(tx_out.address) != str and
           type(tx_out.amount) != int):
            return False
        tx_out_values += tx_out.amount
    # Check if transaction id matches
    if(get_transaction_id(transaction) != transaction.id):
        return False
    # Check if input amount matches output amount
    if(tx_out_values != tx_in_values):
        return False
    return True


def validate_coinbase_transaction(transaction, block_height):
    """
    Validates the coinbase transaction

    Arguments:
    transaction(Transaction) : instance of coinbase transaction
    block_height(int) : height of current block

    Return:
    Boolean : True if valid transaction
    """
    # Check that there is only 1 input transaction
    if(len(transaction.tx_ins) != 1):
        return False
    if(get_transaction_id(transaction) != transaction.id):
        return False
    # Check if tx_out_index is set to current block's height
    if(transaction.tx_ins[0].tx_out_index != block_height):
        return False
    return True


def get_transaction_id(transaction):
    """
    Generate the transaction hash

    Argument:
    transaction(Transaction) : instance of the transaction

    Returns:
    (str) : SHA256 hash of the transaction
    """
    tx_content = ''
    # Do not include signature in the transaction hash
    for tx in transaction.tx_ins:
        tx_content = ''.join(
            [tx_content, tx.tx_out_id, str(tx.tx_out_index)])
    for tx in transaction.tx_outs:
        tx_content = ''.join([tx_content, tx.address, str(tx.amount)])
    return SHA256.new(tx_content.encode('utf-8')).hexdigest()


def generate_coinbase_transaction(block_height, address):
    """
    Generate a coinbase transaction

    Arguments:
    block_height(int) : height of the current block
    address(str) : public key/address to send the coinbase amount

    Return:
    coinbase_tx(Transaction) : coinbase transaction instance
    """
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
