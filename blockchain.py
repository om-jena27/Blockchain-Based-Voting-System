import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, voter_id_hash, candidate_id, previous_hash, eth_tx_hash="N/A"):
        self.index = index
        self.timestamp = timestamp
        self.voter_id_hash = voter_id_hash
        self.candidate_id = candidate_id
        self.previous_hash = previous_hash
        self.eth_tx_hash = eth_tx_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "voter_id_hash": self.voter_id_hash,
            "candidate_id": self.candidate_id,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []

    def load_chain(self, chain_data):
        self.chain = []
        for block_data in chain_data:
            block = Block(
                block_data['index'],
                block_data['timestamp'],
                block_data['voter_id_hash'],
                block_data['candidate_id'],
                block_data['previous_hash'],
                block_data.get('eth_tx_hash', 'N/A')
            )
            block.hash = block_data['hash']
            self.chain.append(block)

    def add_block(self, voter_id_hash, candidate_id, previous_block):
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time(),
            voter_id_hash=voter_id_hash,
            candidate_id=candidate_id,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
