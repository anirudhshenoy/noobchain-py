# Class Block 


1. Block Header
    1. Previous Hash
    2. Merkle Root Hash(?)
    3. Height
    4. Difficulty
    5. Nonce
    6. Unix Timestamp (truncate ms)

2. Data:
   * Transactions in JSON format
   * Strings decoded and stored as bytearray

## Methods: 

1. create_genesis_block 
   * Generates the genesis block with difficulty X, height = 0 
   * Args: previous_hash

2. genereate_next_block:
   * Generates the next block 
   * Args: 
        * previous_hash
        * height
        * difficulty

3. _get_block_header:
   * Return stringified block header
   * Args: self
   * Return -> str

4. calculate_hash: 
    * Return SHA256 hash of header 
    * Args: 
    * Return: hash_string 

5. _has_proof_of_work
    * Check the leading zeros in hash and return true if equal to difficulty level 
    
6. is_valid_hash: 
    * Check if block hash is valid
    * Args: hash_string
    * Return: True/False 

7.  _stringify
    * Json stringify complete block 

8. _get_block
    * Return dict of complete block

# Class : Blockchain
    * self.chain = []
    * store blocks as dicts in hash

1. _is_valid_block_structure
    * Check types of variables in block 
    * Args: instance of Block 
    * Returns: Boolean
    
2. _is_valid_block
    * Check whether height and hash are consistent with previous back
    * calls _is_valid_block_hash and _is_valid_block_structure
    * Args: instance of current block, dict of best block in chain 
    * Returns: boolean

3. _is_valid_block_hash
    * Check whether block_hash received is consistent with block (content + difficulty)
    * Args: instance of current block
    * Returns: Boolean      

4. get_difficulty
    * Adjusts the difficulty at _DIFFICULTY_ADJUSTMENT_INTERVAL based on _BLOCK_INTERVAL_TIME
    * Args: None
    * Returns: Difficulty value for next block

5. get_cummulative_difficulty
    * Get chain difficulty
    * Args: None 
    * Returns: cummulative difficulty