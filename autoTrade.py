import time
import datetime
import json
import trade
import sys

symbol = sys.argv[1]
krw_symbol = "KRW-" + symbol
print("symbol : " + symbol)
print("krw_symbol : " + krw_symbol)

trade.start_auto_trade(symbol)

while True:
    try:
        now = datetime.datetime.now()
        start_time = trade.get_start_time(krw_symbol)
        end_time = start_time + datetime.timedelta(days=1)
        # print(now)
        # print(start_time)
        # print(end_time)

        if if start_time + datetime.timedelta(seconds=360) < now < end_time + datetime.timedelta(seconds=180):
            target_price = trade.get_target_price(krw_symbol, 0.5)
            ma15 = trade.get_ma15(krw_symbol)
            current_price = trade.get_current_price(krw_symbol)
            # print(target_price)
            # print(ma15)
            # print(current_price)
            if target_price < current_price and ma15 < current_price:
                krw = trade.get_balance("KRW")
                if krw > 5000:
                    buy_result = trade.buy_market_order(
                        krw_symbol, krw*0.9995)
                    trade.post_message("#general", symbol +
                                       " buy : " + str(buy_result))
        else:
            balance = trade.get_balance(symbol)
            if balance > float(trade.get_min_quantity(symbol)):
                sell_result = trade.sell_market_order(krw_symbol, balance)
                trade.post_message("#general", symbol +
                                   " sell : " + str(sell_result))
    except TypeError as e:
        # TypeError는 API 호출이 많을때 가끔 발생하니 Pass
        pass
    except Exception as e:
        print(e)
        trade.post_message("#general", symbol + " > Exception")
        trade.post_message("#general", e)
    finally:
        time.sleep(60)
