from Crypto.Hash import SHA256
from time import time
import json


class Block:
    """
    Class: Handles Block creation and utility functions for generating next
    block
    """

    def __init__(self, previous_hash='0', height=0,
                 difficulty=0, nonce=0):
        self.previous_hash = previous_hash
        self.height = height
        self.difficulty = difficulty
        self.nonce = nonce
        self.timestamp = round(time())
        self.data = []

    def create_genesis_block(self, previous_hash='0', difficulty=1):
        self.previous_hash = previous_hash
        self.height = 0
        self.difficulty = difficulty

    def _stringify_block_header(self):
        block_header_json = {
            "previous_hash": self.previous_hash,
            "height": self.height,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
        }
        return json.dumps(block_header_json)

    def __repr__(self):
        return self._stringify_block_header()

    def calculate_hash(self):
        block_header_json = self._stringify_block_header()
        return SHA256.new(block_header_json.encode('utf-8')).hexdigest()

    def _has_proof_of_work(self, difficulty, hash):
        return int(hash[:difficulty], 16) == 0

    def generate_next_block(self, previous_hash, height, difficulty):
        self.previous_hash = previous_hash,
        self.difficulty = difficulty
        self.height = height
        self.block_hash = self.calculate_hash()

        while(not self._has_proof_of_work(self.difficulty, self.block_hash)):
            self.nonce += 1
            self.block_hash = self.calculate_hash()
