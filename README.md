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

# Transactions

## TxIn
    * TxOutId (str)  --> which previous transaction is this In referring to
    * TxOutIndex (int) --> which output in particular
    * signature --> signature to unlock the UTXO

## TxOut
    * Address (str) --> pay to which address
    * Amount (int) --> how much 

## Transaction
    * Id (str) --> transaction hash
    * TxIns [] --> list of TxIn instances
    * TxOuts [] --> list of TxOut instances

 ### Methods
    * _get_transaction_id (self):
        Stringify contents of TxOut and TxIn (without signatures) and hash with SHA256
        Returns: SHA256 Hash

    * sign_input_tx 
        For all txIns, check if a corresponding UTXO exists in the pool. If yes, sign the TxId of the transaction using the private key 

## UTXO
    * TxOutId (str)
    * TxOutIndex (int)
    * address ()
    * amount (int)


## Methods for Transactions 

* update_utxo
    * goes through all waiting transaction:
        * if input of a transaction is currently in UTXO pool, remove it from the pool
        * add all new new transaction outputs to UTXO pool
        
    Args: waiting_transactions [], UTXO_pool []  
    Returns: Updated UTXO_pool

* validate_transaction
    * Check if each transaction: 
        * has valid strcuture
        * all TxIns reference a valid UTXO
        * transaction hash matches ID 
        * TxOutValues matches TxInValues 

    Args: Transaction instance, UTXO_pool
    Returns: True/False

* validate_coinbase_transaction
    * Check if coinbase transaction: 
        * hash matches TxId
        * contains exactly one TxIn
        * the TxOut Index of the only TxIn must equal the block height 

    Args: Transaction instance, block_height
    Returns: True/False

* generate_coinbase_transaction:
    * create new instance of transaction with exactly one input and one output
    * the one input contains the block height as the TXOutId

    Args: block_height, address to transfer coinbase amount
# To-Do 

* add UTXO_pool list to chain
* add waiting_transactions to chain 
* update_UTXO 