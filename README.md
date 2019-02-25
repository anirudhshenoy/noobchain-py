##Class Block 

1)Block Header
    i) Previous Hash
    ii) Merkle Root Hash(?)
    iii) Height
    iv) Difficulty
    v) Nonce
    vi) Unix Timestamp (truncate ms)
2) Data:
    Transactions in JSON format


Strings decoded and stored as bytearray

Methods: 

i) create_genesis_block 
    Generates the genesis block with difficulty X, height = 0 
    Args: previous_hash

ii) genereate_next_block:
    Generates the next block 
    Args: previous_hash
          height
          difficulty

iii) stringify_block_header:
    Return stringified block header
    Args: self
    Return -> str

iv) calculate_hash: 
    Return SHA256 hash of header 
    Args: 
    Return: hash_string 

v) _has_proof_of_work
    Check the leading zeros in hash and return true if equal to difficulty level 
    
v) is_valid_hash: 
    Check if block hash is valid
    Args: hash_string
    Return: True/False 

vi) is_valid_block_structure

