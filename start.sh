#!/bin/bash
source ~/python-env/auto-cryptocurrency-trade/bin/activate

list=("BTT" "LINK" "XLM" "XRP" "ETH" "DOGE" "TRX" "ADA" "ATOM" "MOC" "LAMB" "DOT" "XTZ" "OMG" "EOS" "VET" "CHZ" "META" "MVL" "KMD")

for symbol in "${list[@]}"; do
  { nohup python autoTrade.py "$symbol" > /dev/null & } 2>/dev/null
  sleep 10
done