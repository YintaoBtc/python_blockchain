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
        print(value)
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
    

    
########TEST########
b = Block(index=2, transactions="2", timestamp="ahora", previous_hash="8971232nkl", nonce=0)
print(b)
Block.computed_hash(b)
  


