"python-binance Spot API wrapper and utilities."
import logging
import json
import time

from constants import *
from pathlib import Path
from binance.client import Client
from decimal import Decimal


class Spot_Api():
    def __init__(self, client):
        assert isinstance(client, Client)
        self.__client = client
        self.__log = logging.getLogger("binance_api_wrapper")

    def get_all_tickers(self):
        try:
            return self.__client.get_all_tickers()
        except Exception as err: # pylint: disable=broad-except
            err_msg = f"`get_all_tickers()` failed: {str(err)}"
            self.__log.warning(err_msg)
            return {}

    def get_account(self):
        try:
            return self.__client.get_account()
        except Exception as err: # pylint: disable=broad-except
            err_msg = f"`get_account()` failed: {str(err)}"
            self.__log.warning(err_msg)
            return {}

    def get_balances(self):
        "Get account balances."
        try:
            return self.__client.get_account()['balances']
        except Exception as err: # pylint: disable=broad-except
            msg = f"Could not get account balance:{err}"
            self.__log.warning(msg)
            return None

    def get_step_size(self, symbol):
        """
        Get the step size of the provided trading symbol.

        :param symbol:  Trading symbol
        :type symbol:   str
        """
        try:
            info = self.__client.get_symbol_info(symbol)
        except Exception as err: # pylint: disable=broad-except
            msg = f"Could not get step size for {symbol}:{err}. Defaulting to 0.001"
            self.__log.warning(msg)
            return Decimal("0.001") # TODO(rouxam) find a better default value or throw
        else:
            if info is not None:
                for filt in info["filters"]:
                    if filt["filterType"] == "LOT_SIZE":
                        return Decimal(filt["stepSize"]).normalize()
        msg = f"Could not get step size for {symbol}. Defaulting to 0.001"
        self.__log.warning(msg)
        return Decimal("0.001") # TODO(rouxam) find a better default value or throw

    def order_market_buy(self, symbol, quantity):
        "Create market buy order on spot account."
        quantity = float(quantity)
        msg = f"MARKET BUY {quantity} {symbol}"
        self.__log.info(msg)
        try:
            _ = self.__client.order_market_buy(symbol=symbol, quantity=quantity)
        except Exception as err: # pylint: disable=broad-except
            err_msg = f"`order_market_buy()` failed: {str(err)}"
            self.__log.warning(err_msg)

    def order_market_sell(self, symbol, quantity):
        "Create market buy order on spot account."
        quantity = float(quantity)
        msg = f"MARKET SELL {quantity} {symbol}"
        self.__log.info(msg)
        try:
            _ = self.__client.order_market_sell(symbol=symbol, quantity=quantity)
        except Exception as err: # pylint: disable=broad-except
            err_msg = f"`order_market_sell()` failed: {str(err)}"
            self.__log.warning(err_msg)

    def get_historical_klines(self, **args):
        "Create market buy order on spot account."
        try:
            ret = self.__client.get_historical_klines(**args)
        except Exception as err: # pylint: disable=broad-except
            err_msg = f"`order_market_sell()` failed: {str(err)}"
            self.__log.warning(err_msg)
            ret = []
        return ret

    def get_all_orders(self, symbol):
        "Get all orders on symbol."
        try:
            ret = self.__client.get_all_orders(symbol=symbol)
        except Exception as err: # pylint: disable=broad-except
            err_msg = f"`get_all_orders()` failed: {str(err)}"
            self.__log.warning(err_msg)
            ret = []
        return ret
