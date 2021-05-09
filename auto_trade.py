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

        # 9시 3분 ~ 6분 사이에 전량 매도, 이외에는 매수 로직
        if start_time + datetime.timedelta(seconds=360) < now < end_time + datetime.timedelta(seconds=180):
            target_price = trade.get_target_price(krw_symbol, 0.5)
            ma15 = trade.get_ma15(krw_symbol)
            current_price = trade.get_current_price(krw_symbol)
            emergency_price = trade.get_emergency_price(symbol)
            # print(target_price)
            # print(ma15)
            # print(current_price)
            # print(emergency_price)

            # 현재가격이 위험가격 밑으로 떨어지면 전량 매도
            if emergency_price > current_price:
                trade.execute_sell(krw_symbol, symbol)
            # 현재가가 변동성돌파전략 가격보다 크고 이동성 평균값보다 크면 매수
            elif target_price < current_price and ma15 < current_price:
                trade.execute_buy(krw_symbol, symbol)
        else:
            # 전량 매도
            trade.execute_sell(krw_symbol, symbol)
    except TypeError as e:
        # TypeError는 API 호출이 많을때 가끔 발생하니 Pass
        pass
    except Exception as e:
        print(e)
        trade.post_message("#general", symbol + " > Exception")
        trade.post_message("#general", e)
    finally:
        time.sleep(60)
