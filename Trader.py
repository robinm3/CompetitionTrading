
import threading
import time
import math
from datetime import timedelta

import numpy as np

class Trader:
    
    """
    
    
    Implantez ici votre algorithme de trading. Le marche est accessible avec la
    variable Market. Les differentes fonctions disponibles sont disponibles dans
    le fichier API et expliquees dans le document de la competition
    """
    
    #Nom de l'equipe:
    equipe = 'Purple goats'

    def __init__(self, API):
        
        self.API = API
        self.API.setEquipe(self.equipe)

        self.short_ema_window = 3
        self.medium_ema_window = 7  # 6
        self.buy_price = -1
        self.last_stock_price = -1
        
    """Function called at start of run"""
    def run(self):
        
        """You can add initialization code here"""
        
        
        self.t = threading.currentThread()
        while getattr(self.t, "run", True):
            try:
                self.trade()
            except Exception as e:
                print(e)
                pass
            time.sleep(0)

    """Your trading algorithm goes here!
        The function is called continuously"""
    def trade(self):
        first_stonk = 'LAL'
        money_left = self.API.getUserCash()
        price = self.API.getPrice(first_stonk)
        if self.last_stock_price == price:
            return
        self.last_stock_price = price
        max_to_buy = math.floor(money_left / price)

        print(taux)
        if(taux > 2):
            self.API.marketBuy(first_stonk, max_to_buy)
        if(taux < -3):
            self.API.marketSell(first_stonk, self.API.getUserStocks()[first_stonk])


        # short_ema = self.get_short_ema(first_stonk)
        # medium_ema = self.get_medium_ema(first_stonk)
        #
        # if short_ema != -1 and medium_ema != -1:
        #     price = self.API.getPrice(first_stonk)
        #     money_left = self.API.getUserCash()
        #
        #     if short_ema > medium_ema:
        #         max_to_buy = math.floor(money_left / price)
        #         self.API.marketBuy(first_stonk, max_to_buy)
        #         self.buy_price = price
        #
        #     if self.buy_price != -1:
        #         taux = self.taux_evolution(self.buy_price, price)
        #         #print(taux)
        #         if np.abs(taux) > 0.02:
        #             #print("Je vends")
        #             self.API.marketSell(first_stonk, self.API.getUserStocks()[first_stonk])
        #             self.buy_price = -1
        #             #print("J ai vendu")

        # if(money_left > 1000):
        #     max_to_buy = math.floor(money_left / price)
        #     self.API.marketBuy(first_stonk, max_to_buy)

    def get_taux(self, stonk, time_variation):
        past_prices = self.API.getPastPrice(stonk, self.API.getTime() - time_variation, self.API.getTime())
        prices = []
        for time, price in past_prices.items():
            prices.append(float(price))

        return self.taux_evolution(prices[0], prices[-1])


    def get_short_ema(self, action):
        current_time = self.API.getTime()
        debut = current_time - timedelta(hours=0, minutes=120)
        response = self.API.getPastPrice(action, debut, current_time)
        short_price = []

        for time, price in response.items():
            short_price.append(float(price))

        if len(short_price) <= self.short_ema_window:
            return -1

        return self.ema(short_price, self.short_ema_window)

    def get_medium_ema(self, action):
        current_time = self.API.getTime()
        debut = current_time - timedelta(hours=0, minutes=240)
        response = self.API.getPastPrice(action, debut, current_time)
        medium_price = []

        for time, price in response.items():
            medium_price.append(float(price))

        if len(medium_price) <= self.medium_ema_window:
            return -1

        return self.ema(medium_price, self.medium_ema_window)

    def ema(self, values, window):
        weight = np.repeat(1.0, window) / window
        weight /= weight.sum()
        x = np.convolve(values, weight)[:len(values)]
        x[:window] = x[window]
        return x[-1]

    def taux_evolution(self, initial, final) -> float:
        return ((final - initial) / initial) * 100.0