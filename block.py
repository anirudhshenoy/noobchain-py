from Crypto.Hash import SHA256
from time import time
import json


class Block:
    """
    Class: Handles Block creation and utility functions for generating next
    block
    """

    def __init__(self, block_hash='0', previous_hash='0', height=0,
                 difficulty=0, nonce=0):
        self.previous_hash = previous_hash
        self.height = height
        self.difficulty = difficulty
        self.nonce = nonce
        self.timestamp = round(time())
        self.data = []
        self.block_hash = block_hash

    def create_genesis_block(self, previous_hash='0', difficulty=1):
        self.previous_hash = previous_hash
        self.height = 0
        self.difficulty = difficulty
        self.block_hash = self.calculate_hash()
        self._mine_block()

    def _get_block_header(self):
        block_header_json = {
            "previous_hash": self.previous_hash,
            "height": self.height,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
        }
        return block_header_json

    def _get_block_json(self):
        block_json = self._get_block_header()
        block_json.update({
            'block_hash': self.block_hash,
            'data': self.data,
        })
        return block_json

    def _stringify(self, json_object):
        return json.dumps(json_object)

    def __repr__(self):
        return self._stringify(self._get_block_json())

    def __str__(self):
        return self._stringify(self._get_block_json())

    def calculate_hash(self):
        block_header_json = self._stringify(self._get_block_header())
        return SHA256.new(block_header_json.encode('utf-8')).hexdigest()

    def _has_proof_of_work(self, difficulty, hash):
        return int(hash[:difficulty], 16) == 0

    def generate_next_block(self, previous_hash, height, difficulty):
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.height = height
        self.block_hash = self.calculate_hash()
        self._mine_block()

    def _mine_block(self):
        while(not self._has_proof_of_work(self.difficulty, self.block_hash)):
            self.nonce += 1
            self.block_hash = self.calculate_hash()
