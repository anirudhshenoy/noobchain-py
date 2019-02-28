from block import Block
import json
from pprint import pprint
import time


class Blockchain:
    """
    Class: Generates new blocks and adds to array
    """

    def __init__(self, chain=[]):
        self.chain = chain
        self._BLOCK_INTERVAL_TIME_SECS = 30
        self._DIFFICULTY_ADJUSTMENT_INTERVAL = 10

    def _is_valid_block_structure(self, block):
        return (type(block.previous_hash) == str and
                type(block.height) == int and
                type(block.difficulty) == int and
                type(block.nonce) == int and
                type(block.timestamp) == int and
                type(block.data) == list and
                type(block.block_hash) == str)

    def _is_valid_block_hash(self, block):
        if(block.calculate_hash() != block.block_hash):
            return False
        if(int(block.block_hash[:block.difficulty], 16) != 0):
            return False
        return True

    def is_valid_block(self, block, previous_block):
        if(previous_block['block_hash'] != block.previous_hash):
            print('Invalid Hash')
            return False
        if(previous_block['height']+1 != block.height):
            print('Invalid Height')
            return False
        if not(self._is_valid_block_hash(block) and
                self._is_valid_block_structure(block)):
            print('Strucutre Invalid')
            return False
        return True

    def push_genesis_block(self, previous_hash, difficulty):
        if(len(self.chain)):
            print('Genesis block already exists')
            return False
        genesis_block = Block()
        genesis_block.create_genesis_block(previous_hash, difficulty)
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
        new_block.generate_next_block(
            previous_block['block_hash'],
            previous_block['height']+1,
            self.get_difficulty(),
        )
        if(self.is_valid_block(new_block, previous_block)):
            self.chain.append(str(new_block))
            return True
        return False

    def get_block_from_height(self, height):
        """
        Search for block matching 'height'
        Returns: Block if exists, false if not
        Args: Height(int)
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
        try:
            return json.loads(self.chain[len(self.chain)-1:][0])
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

            if(expected_time_interval < actual_time_interval*2):
                return best_block['difficulty'] - 1
            elif(expected_time_interval >= actual_time_interval/2):
                return best_block['difficulty'] + 1
        else:
            return best_block['difficulty']

    def get_cummulative_difficulty(self):
        cummulative_difficulty = 0
        for i in range(len(self.chain)):
            block_difficulty = self.get_block_from_height(i)['difficulty']
            cummulative_difficulty += 2**block_difficulty
        return cummulative_difficulty

if __name__ == '__main__':
    chain = Blockchain()
    chain.push_genesis_block('helloWorld', 2)

    for i in range(99):
        chain.generate_block_and_push()
        # pprint(chain.get_best_block())
    # print(chain.get_block_from_height(1))
    print(chain.get_difficulty())
