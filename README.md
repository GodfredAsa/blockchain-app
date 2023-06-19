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


