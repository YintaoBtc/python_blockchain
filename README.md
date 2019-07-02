# Blockchain en python

Blockchain en python desde 0. Con la ayuda del tutorial:
<https://recursospython.com/guias-y-manuales/aplicacion-blockchain-desde-cero/>

## Versión 0.1  

- Crear la class Block con:
    1. index
    2. transactions
    3. timestamp
    4. previous_hash
    5. nonce
- Block tambien tiene la funcion compute_hash que nos devuelve un hash del Block
- Crear la class Blockchain para poder añadir los Blocks que vamos creando.
    1. unconfirmed_transaction
    2. difficulty
    3. create_genesis_block
    4. last_block
- Añadida Proof of Work dentro de la class Blockchain

## Versión 0.2

- Se pueden añadir bloques con add_block
    1. block
    2. proof
- Minado funcionando. Permite Añadir las transferencias de un pool para formar el bloque y depues hace el proof of work
    1. add_new_transaction
    2. new_block
    3. proof_of_work
    4. unconfirmed_transactions = []

## Versión 0.3

- Añadida app Flask para mostrar en navegador. 
- Añadidas las siguientes paginas.
    1. /new_transaction
    2. /chain
    3. /mine
    4. /pending_tx
    5. /add_nodes
    6. /add_block
- Añadido consenso que mide el largo de las cadenas.
- Se puede probar con el comando:

```python yincoin.py
```
