from Crypto.Hash import SHA256
from time import time
import json
import transaction


class Block:
    """
    Class: Handles Block creation and utility functions for generating next
    block
    """

    def __init__(self, data=[], block_hash='0', previous_hash='0', height=0,
                 difficulty=0, nonce=0):
        """
        Constructor for Block
        Arguments:
        data(list) : List of transaction objects
        block_hash(str) : Hash of the block
        previous_hash(str) : Hash of the previous block
        height(int) : Height of the current block
        difficulty(int) : Difficulty of block  - # of leading zeros for mining
        nonce(int) : nonce for block - usually automatically set by mining
        """
        self.previous_hash = previous_hash
        self.height = height
        self.difficulty = difficulty
        self.nonce = nonce
        self.timestamp = round(time())
        self.data = data
        self.block_hash = block_hash

    def create_genesis_block(self, data=[], previous_hash='0', difficulty=1):
        """
        Creates and mines the genesis block in the chain

        Arguments:
        data(list) : Array of transaction objects to be included in the block
        previous_hash(str) : Hash to initialize genesis block
        difficulty(int) : difficulty of block
        """
        self.previous_hash = previous_hash
        self.height = 1
        self.difficulty = difficulty
        self.data = data
        self.block_hash = self.calculate_hash()
        self._mine_block()

    def _get_block_header(self):
        """
        Returns a dict containing variables from the block header

        Arguments:
        None

        Returns:
        block_header_json(dict)
        """
        block_header_json = {
            "previous_hash": self.previous_hash,
            "height": self.height,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
        }
        return block_header_json

    def _get_block_json(self):
        """
        Returns dict of the entire block in JSON format

        Arguments:
        None

        Returns:
        block_json(dict) containing all variables from the block
        """
        data_json = []
        #create an array of transaction JSON objects
        for i in range(len(self.data)):
            data_json.append(self.data[i].get_json())
        block_json = self._get_block_header()
        block_json.update({                #Add block_hash and data to block header dict
            'block_hash': self.block_hash,
            'data': data_json,
        })
        return block_json

    def _stringify(self, json_object):
        """
        Stringified JSON object 
        """
        return json.dumps(json_object)

    def __repr__(self):
        return self._stringify(self._get_block_json())

    def __str__(self):
        return self._stringify(self._get_block_json())

    def calculate_hash(self):
        """
        Return SHA256 hash of the blockk header
        
        Arguments:
        None

        Returns:
        Hash(str) 
        """
        block_header_json = self._stringify(self._get_block_header())
        return SHA256.new(block_header_json.encode('utf-8')).hexdigest()

    def _has_proof_of_work(self, difficulty, hash):
        """
        Checks if the current hash matches the difficulty

        Arguments:
        difficulty(int) : difficulty of current block 
        hash(str): current hash of the block 

        Returns:
        Boolean : True if difficulty matches current hash
        """
        return int(hash[:difficulty], 16) == 0

    def generate_next_block(self, data, previous_hash, height, difficulty):
        """
        Creates and mines the next block

        Arguments:
        data(list) : list of transaction objects
        previous_hash(str) : hash of the previous block 
        height(int) : height of the current block 
        difficulty(int) : difficulty for mining

        Returns:
        None
        """
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.height = height
        self.data = data
        self.block_hash = self.calculate_hash()
        self._mine_block()

    def _mine_block(self):
        """
        Mines the current block

        Arguments:
        None

        Returns:
        None
        """
        while(not self._has_proof_of_work(self.difficulty, self.block_hash)):
            self.nonce += 1             #increment nonce until _has_proof_of_work returns True
            self.block_hash = self.calculate_hash()
