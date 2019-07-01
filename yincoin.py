from hashlib import sha256
import json, time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce):
        self.index = index 
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce



    def computed_hash(self):
        """Funcion que crea el hash del bloque"""

        block_string = json.dumps(self.__dict__, sort_keys=True)
        value = sha256(block_string.encode()).hexdigest()
        return value


class Blockchain:

    # Dificultad del algoritmo de prueba de trabajo.
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = [] # información para insertar en el blockchain
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """ 
        Una función para generar el bloque génesis y añadirlo a la 
        cadena. El bloque tiene index 0, previous_hash 0 y un hash
        válido.
        """
        genesis_block = Block(0, [], time.time(), "0", 0)
        genesis_block.hash = genesis_block.computed_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Función que intenta distintos valores de nonce hasta obtener
        un hash que satisfaga el criterio de dificultad.
        """

        block.nonce = 0
        computed_hash = block.computed_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.computed_hash()

        return computed_hash
    
    def add_block(self, block, proof):
        """
        Función que añade un bloque despues de verificarlo
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False
        
        if not self.is_valid_proof(block, proof):
            return False
        
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Funcion que checkea si el block_hash es valido
        """
        return(block_hash.startswith("0" * Blockchain.difficulty)and block_hash == block.compute_hash())


    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction) 

    def mine(self):
        """
        Funcion que busca unconfirmed transactions para minarlas en un bloque.
        """

        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block

        new_bock = Block(index=last_block.index + 1,
                        transactions=self.unconfirmed_transactions,
                        timestamp = time.time(),
                        previous_hash = last_block.hash
        )

        proof = self.proof_of_work(new_bock)
        self.add_block(new_bock, proof)

        self.unconfirmed_transactions = []
        return new_bock.index
    

    
########TEST########
b = Block(index=2, transactions="2", timestamp="ahora", previous_hash="8971232nkl", nonce=0)
x = Block.computed_hash(b)
print(f"Este es el hash del Block:\n{x}")
  


