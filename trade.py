import time
import pyupbit
import datetime
import requests
import json

access = "access"
secret = "secret"
slackToken = "slack"

upbit = pyupbit.Upbit(access, secret)


def start_auto_trade(symbol):
    print(symbol + "Auto Trade Start")
    post_message("#general", symbol + " Auto Trade Start")
    balances = upbit.get_balances()
    print(json.dumps(balances))
    post_message("#general", json.dumps(balances))


def buy_market_order(ticker, krw):
    return upbit.buy_market_order(ticker, krw)


def sell_market_order(ticker, quantity):
    return upbit.sell_market_order(ticker, quantity)


def post_message(channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer "+slackToken},
                             data={"channel": channel, "text": text}
                             )


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


def get_min_quantity(symbol):
    price = pyupbit.get_current_price("KRW-"+symbol)
    return "%2.5f" % (5000/price)
