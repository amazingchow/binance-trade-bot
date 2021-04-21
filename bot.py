# -*- coding: utf-8 -*-
import coloredlogs
import datetime
import logging
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger, fmt="[%(asctime)s][%(levelname)s] %(message)s")
import os
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from binance.client import Client
from binance.exceptions import BinanceAPIException

class BinanceTradeClient():
    '''
    币安打新机器人

    币安API根地址: https://api.binance.com/api/v3/
    '''
    def __init__(self, ak: str, sk: str, proxies: dict):
        self.cli = Client(api_key=ak, api_secret=sk, requests_params={"proxies": proxies, "verify": False, "timeout": 10})
    
    def is_ready(self):
        '''
        测试网络时延: httpstat https://api.binance.com/api/v3/ping
        '''
        ready = True
        try:
            self.cli.ping()
        except BinanceAPIException as e:
            logger.error("failed to setup the binance-trade-bot, err: {}.".format(e))
            ready = False
        finally:
            return ready

    def buy_market_ticker_price(self, sym: str, quantity: float):
        '''
        buy some quantities of a specific coin, like sym == PHABUSD
        '''
        try:
            self.cli.order_market_buy(symbol=sym, quoteOrderQty=quantity, recvWindow=1000)
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    ak = os.getenv("BINANCE_MAINNET_API_KEY")
    sk = os.getenv("BINANCE_MAINNET_SECRET_KEY")
    if ak == None or sk == None:
        logger.critical("please provide BINANCE_MAINNET_API_KEY and BINANCE_MAINNET_SECRET_KEY first")
    
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")
    if http_proxy == None or https_proxy == None:
        logger.critical("please provide HTTP_PROXY and HTTPS_PROXY first")
    proxies = {
        "http": http_proxy,
        "https": https_proxy
    }

    bot = BinanceTradeClient(ak=ak, sk=sk, proxies=proxies)
    while not bot.is_ready():
        time.sleep(2)
    logger.info("binance-trade-bot has got ready!!!")
    
    # 根据实际情况来修改上新时间, 这里的上新时间为2021年4月21号下午6点整.
    new_arrival_time = datetime.datetime(2021, 4, 21, 18, 0).timestamp()

    now = time.time()
    while now < new_arrival_time:
        time.sleep(0.001)
        now = time.time()

    # !!!在现货钱包里只留900 BUSD.
    # 购入价值600 BUSD的BAR, 尝试连续购买5次.
    cnt = 0
    while cnt < 6:
        bot.buy_market_ticker_price("BARBUSD", 600)
        time.sleep(0.01)
        cnt += 1
     