import time
import datetime
import json
import trade
import sys

symbol = sys.argv[1]
ticker = "KRW-" + symbol
print("symbol : " + symbol)
print("ticker : " + ticker)

trade.start_auto_trade(symbol)

while True:
    try:
        now = datetime.datetime.now()
        start_time = trade.get_start_time(ticker)
        end_time = start_time + datetime.timedelta(days=1)
        # print(now)
        # print(start_time)
        # print(end_time)

        # 8시 58분 ~ 9시 사이에 전량 매도, 이외에는 매수 로직
        if start_time < now < end_time - datetime.timedelta(seconds=120):
            target_price = trade.get_target_price(ticker, 0.3)
            ma15 = trade.get_ma15(ticker)
            current_price = trade.get_current_price(ticker)
            emergency_price = trade.get_emergency_price(symbol)
            # print(target_price)
            # print(ma15)
            # print(current_price)
            # print(emergency_price)

            # 현재가격이 위험가격 밑으로 떨어지면 전량 매도
            if emergency_price > current_price:
                trade.execute_sell(ticker, symbol)
            # 현재가가 변동성돌파전략 가격보다 크고 이동성 평균값보다 크면 매수
            elif target_price < current_price and ma15 < current_price:
                trade.execute_buy(ticker, symbol)
        else:
            # 전량 매도
            trade.execute_sell(ticker, symbol)
    except TypeError as e:
        # TypeError는 API 호출이 많을때 가끔 발생하니 Pass
        pass
    except Exception as e:
        print(e)
        trade.post_message("#general", symbol + " > Exception")
        trade.post_message("#general", e)
    finally:
        time.sleep(60)
