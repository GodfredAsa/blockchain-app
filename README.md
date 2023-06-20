***CREATING VIRTUAL ENVIRONMENT***
```pip3 install venv <virtual_name>```
Example Below 
```pip3 install venv blockchain-env```

***ACTIVATE THE VIRTUAL ENV**
```source blockchain-env/bin/activate ```

***INSTALL ALL PACKAGES OR DEPENDENCIES**
```pip3 install -r requirements.txt```


***RUN THE TESTS**

Activate the virtual environment as described above 
```python3 -m pytest backend/tests ```

<!-- command for running modules or files  -->
```python -m backend.blockchain.block ```
<!-- running average block rate file  -->
```python3 -m backend.scripts.average_block_rate```
<!-- running conversion rate file  -->
```python3 -m backend.utils.hex_to_binary```


#### Chain Validation 
1. its the concept of inspecting a blockchain has been constructed correctly 
2. chain replacement is the process when an old block is replaced with a new block which mostly longer than the previous. Chain replacement is necessary a block should be built from other blocks. when multiple blocks interact with each other its called a blockchain network.