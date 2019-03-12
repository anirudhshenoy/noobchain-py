from block import Block
import json
from pprint import pprint
import time
import transaction as tx
import ecdsa as ec

# private_key = 799bbb0994f25b0596d10b3414471ddcf4da38e41ace54cfba2983e23ec26e99

COINBASE_ADDRESS = '1473d4597cfa0bdbbf5a7dc3ff51e7de14ded14bcc863c479e44c66a06308d475145ee8a0db11e35fd51efc797015f09a7499494980b70eb0e6253591620119a'


class Blockchain:
    """
    Class: Generates new blocks and adds to array
    """

    def __init__(self, chain=[]):
        self.waiting_transactions = []
        self.UTXO_pool = []
        self.chain = chain
        # Constant to determine difficulty adjustment interval
        self._BLOCK_INTERVAL_TIME_SECS = 30
        self._DIFFICULTY_ADJUSTMENT_INTERVAL = 10

    def _is_valid_block_structure(self, block):
        """
        Checks the structure of the block

        Arguments:
        block (Block) : instance of block 

        Returns:
        Boolean: True if structure is corrent
        """
        return (type(block.previous_hash) == str and
                type(block.height) == int and
                type(block.difficulty) == int and
                type(block.nonce) == int and
                type(block.timestamp) == int and
                type(block.data) == list and
                type(block.block_hash) == str)

    def _is_valid_block_hash(self, block):
        """
        Checks if the block hashes to the value in block_hash
        Checks if hash matches difficulty

        Arguments:
        block(Block) : instance of block 

        Returns:
        Boolean : True if match
        """

        # Check if block_hash matches block header hash
        if(block.calculate_hash() != block.block_hash):
            return False
        # Check if hash matches difficulty of block
        if(int(block.block_hash[:block.difficulty], 16) != 0):
            return False
        return True

    def is_valid_block(self, block, previous_block):
        """
        Check if the new block is valid

        Arguments:
        block(Block) : instance of current block 
        previous_block(Block): instance of previous_block

        Returns:
        Boolean: True if valid block
        """
        # Check if previous_hash matches previous blocks hash
        if(previous_block['block_hash'] != block.previous_hash):
            print('Invalid Hash')
            return False
        # Check if height is 1 above previous height
        if(previous_block['height']+1 != block.height):
            print('Invalid Height')
            return False
        # Check block hash and structure
        if not(self._is_valid_block_hash(block) and
                self._is_valid_block_structure(block)):
            print('Strucutre Invalid')
            return False
        return True

    def _update_UTXO(self):  # TODO
        """
        Iterate through all transactions in waiting_transactions and update
        UTXO_pool

        Arguments:
        None
        """
        for transaction in self.waiting_transactions:
            for tx_in in transaction.tx_ins:
                for i in range(len(self.UTXO_pool)):
                    # Delete UTXOs that have been spent
                    self.UTXO_pool = [
                        x for x in self.UTXO_pool if x.tx_id != tx_in.tx_out_id]
            for idx, tx_out in enumerate(transaction.tx_outs):
                new_utxo = tx.UTXO(transaction.id, idx,
                                   tx_out.address, tx_out.amount)
                self.UTXO_pool.append(new_utxo)
        self.waiting_transactions = []

    def get_UTXO_json(self):
        """
        Get list of UTXO JSON dicts

        Returns:
        utxo_stringified(list) 
        """
        utxo_stringified = [utxo.get_json() for utxo in self.UTXO_pool]
        return utxo_stringified

    def add_transaction(self, transaction):
        """
        Adds the transaction to waiting_transactions list
        Arguments:
        transaction(Transaction) : transaction object
        Returns: True if transaction has been added to waiting_transaction
        """
        if(tx.validate_transaction(transaction, self.UTXO_pool)):
            self.waiting_transactions.append(transaction)
            return True
        return False

    def _generate_coinbase_transaction(self, height):
        """
        Generates a coinbase transaction validate and add to
        waiting_transactions

        Arguments:
        height(int) : current block height

        Returns: None
        """
        coinbase_transaction = tx.generate_coinbase_transaction(
            height, COINBASE_ADDRESS)
        coinbase_transaction.generate_tx_hash()
        # Validate and add coinbase transaction at index 0 of
        # waiting_transactions
        if(tx.validate_coinbase_transaction(coinbase_transaction, height)):
            self.waiting_transactions.insert(0, coinbase_transaction)

    def push_genesis_block(self, previous_hash, difficulty):
        """
        Generate the genesis block

        Arguments:
        previous_hash(str) : hash to initalize block
        difficulty(int) : difficulty of block

        Returns:
        Boolean: True if block succesfully added
        """
        # Create genesis block only if chain is empty
        if(len(self.chain)):
            print('Genesis block already exists')
            return False
        genesis_block = Block()
        self._generate_coinbase_transaction(1)
        # Pass empty list - Genesis block can't have transactions
        # except coinbase
        genesis_block.create_genesis_block(
            [], previous_hash, difficulty)
        self._update_UTXO()
        self.chain.append(str(genesis_block))
        return True

    def generate_block_and_push(self):
        """
        Create a new instance of Block, pass previous_blocks parameters.
        Validate the new block and push to existing chain

        Returns: True if block generated and pushed succesfully
        """
        new_block = Block()
        previous_block = self.get_best_block()
        self._generate_coinbase_transaction(previous_block['height']+1)
        new_block.generate_next_block(
            self.waiting_transactions,
            previous_block['block_hash'],
            previous_block['height']+1,
            self.get_difficulty(),
        )
        if(self.is_valid_block(new_block, previous_block)):
            self.chain.append(str(new_block))
            self._update_UTXO()
            return True
        return False

    def get_block_from_height(self, height):
        """
        Search for block matching 'height'
        Args: Height(int) 

        Returns: Block in JSON format if exists, false if not
        """
        try:
            block = json.loads(self.chain[height-1])
        except:
            print('Index out of bounds')
            return False
        return block

    def __len__(self):
        return len(self.chain)

    def __repr__(self):
        return str(self.chain)

    def get_best_block(self):
        """
        Gets the best block from chain 

        Args: None

        Returns:
        Best block in JSON format if genesis block has been mined
        """
        try:
            return json.loads(self.chain[len(self.chain)-1])
        except IndexError:
            raise IndexError('Genesis Block does not exist')

    def get_difficulty(self):
        """
        Adjusts the difficulty at _DIFFICULTY_ADJUSTMENT_INTERVAL based on
        _BLOCK_INTERVAL_TIME
        Args: None
        Returns: Difficulty value for next block
        """
        best_block = self.get_best_block()
        # New interval, check whether we need to adjust difficulty
        if(best_block['height'] % self._DIFFICULTY_ADJUSTMENT_INTERVAL == 0):
            expected_time_interval = self._BLOCK_INTERVAL_TIME_SECS * \
                self._DIFFICULTY_ADJUSTMENT_INTERVAL
            previous_adjusted_timestamp = self.get_block_from_height(
                best_block['height']-self._DIFFICULTY_ADJUSTMENT_INTERVAL)['timestamp']
            actual_time_interval = best_block[
                'timestamp'] - previous_adjusted_timestamp

            # if time taken is 2 times more than expected time, reduce
            # difficulty by 1
            if(expected_time_interval < actual_time_interval*2):
                return best_block['difficulty'] - 1
            # if half of time taken is less than expected time increase
            # difficulty by 1
            elif(expected_time_interval >= actual_time_interval/2):
                return best_block['difficulty'] + 1
        else:
            return best_block['difficulty']

    def get_cummulative_difficulty(self):
        """
        Get cummulative difficulty of all blocks

        """
        cummulative_difficulty = 0
        for i in range(len(self.chain)):
            block_difficulty = self.get_block_from_height(i)['difficulty']
            cummulative_difficulty += 2**block_difficulty
        return cummulative_difficulty


def print_balance(address):
    utxo = chain.get_UTXO_json()
    balance = 0
    for tx in utxo:
        if tx['address'] == address:
            balance += tx['amount']
    print(balance)


if __name__ == '__main__':
    chain = Blockchain()
    chain.push_genesis_block('helloWorld', 2)
    for i in range(9):
        chain.generate_block_and_push()
    # pprint(chain.get_best_block())
    # print(chain.get_UTXO_json())
    t = tx.Transaction()
    t.push_tx_in(
        '335ce2fc05ae6df463065ceca34075a6a51acdbe0c36a2433ab3b2634f9727f4', 0)
    t.push_tx_out('HelloBob', 40)
    t.push_tx_out(COINBASE_ADDRESS, 10)
    t.id = tx.get_transaction_id(t)
    t.sign_input_txs(
        '799bbb0994f25b0596d10b3414471ddcf4da38e41ace54cfba2983e23ec26e99', chain.UTXO_pool)
    # print(t.get_json())
    chain.add_transaction(t)
    # print(chain.waiting_transactions)
    chain.generate_block_and_push()
    # print(chain.get_UTXO_json())
    print_balance('HelloBob')
    print_balance(COINBASE_ADDRESS)
