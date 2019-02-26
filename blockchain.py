from block import Block


class Blockchain:
    """
    Class: Generates new blocks and adds to array
    """

    def __init__(self, chain=[]):
        self.chain = chain

    def _is_valid_block_structure(block):
        return (type(block.previous_hash) == str and
                type(block.height) == int and
                type(block.difficulty) == int and
                type(block.nonce) == int and
                type(block.timestamp) == int and
                type(block.data) == list and
                type(block.block_hash) == str)

    def _is_valid_block_hash(block):
        if(block.calculate_hash() != block.block_hash):
            return False
        if(int(block.block_hash[:block.difficulty], 16) != 0):
            return False
        return True

    def is_valid_block(block, previous_block):
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

    def push_block(block):
        pass
