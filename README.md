# Auto Trade - Crypto Currency

## virtualenv

### virtualenv -p python3 ~/python-env/auto-cryptocurrency-trade

### source ~/python-env/auto-cryptocurrency-trade/bin/activate

pip install -U pyupbit

pip freeze > requirements.txt

### pip install -r requirements.txt

## start trade

- sh gogogo.sh
- ( nohup python autoTrade.py ETH > output-eth.log & )

## quit trade

- ps ax | grep autoTrade | awk '{print $1}' | xargs kill
