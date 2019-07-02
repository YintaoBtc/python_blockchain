from hashlib import sha256
import json, time
from flask import Flask, request
import requests

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
  

app =  Flask(__name__)
 
# la copia del nodo del blockchain
blockchain = Blockchain()


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invlaid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201

@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    
    return json.dumps({
        "length": len(chain_data),
        "chain": chain_data
    })

@app.route("/mine", methods=["GET"])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No hay transacciones para minar"
    
    return "Block #{result} minado correctamente."

@app.route("/pending_tx")
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

app.run(debug=True, port=8000)

blockchain.create_genesis_block()

#Otros nodes de la red
peers = set()

#Interfaz para unir mas nodes
@app.route("/add_nodes", methods=["POST"])
def register_new_peers():
    nodes = request.get_json()
    if not nodes:
        return "Invalid data", 400

    for node in nodes:
        peers.add(node)

    return "Success", 201

#La cadena mas larga es la cadena buena
def consensus():

    global blockchain

    longest_chain = None
    current_len = len(blockchain)

    for node in peers:
        response = requests.get(f'http://{node}/chain')
        length = response.json()["length"]
        chain = response.json()["chain"]
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

        if longest_chain:
            blockchain = longest_chain
            return True
        
        return False

    
@app.route("/add_block", methods=["POST"])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                block_data["transactions"],
                block_data["timestamp"], 
                block_data["previous_hash"])

    proof = block_data["hash"]
    added = blockchain.add_block(block, proof)

    if not added:
        return "Bloque descartado por el node"

    return "Bloque añadido a la cadena"

def announce_new_block(block):
    for peer in peers:
        url = "http://{}/add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))
