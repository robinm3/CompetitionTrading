
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
        self.buy_action = None
        
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
        stonks = self.API.getListStocks()
        first_stonk = stonks[0]
        coeff = 0.0
        current_time = self.API.getTime()

        short_ema = self.get_short_ema(first_stonk)
        medium_ema = self.get_medium_ema(first_stonk)

        if self.buy_price == -1:
            multiple_coeff = {}
            for action in stonks:
                if action != "ETF":
                    last_prices = self.get_last_prices(action, current_time)
                    action_coeff = self.compute_trend(last_prices)
                    multiple_coeff[action] = action_coeff

            best_coeff = -1
            best_action = ""
            for action, coeff in multiple_coeff.items():
                if coeff > best_coeff:
                    best_coeff = coeff
                    best_action = action

            first_stonk = best_action
            coeff = best_coeff
        else:
            current_price_action = self.get_last_prices(self.buy_action, current_time)
            coeff = self.compute_trend(current_price_action)
            #first_stonk = self.buy_action

        if short_ema != -1 and medium_ema != -1:
            price = self.API.getPrice(first_stonk)
            money_left = self.API.getUserCash()

            if self.buy_price == -1:  # Buy
                if short_ema > medium_ema and coeff > 0.005:
                    max_to_buy = math.floor(money_left / price)
                    self.API.marketBuy(first_stonk, max_to_buy)
                    self.buy_price = price
                    self.buy_action = first_stonk
                    print("Achat")
            else:  # Sell
                if self.buy_price != -1:
                    taux = self.taux_evolution(self.buy_price, price)
                    if taux < -0.02 or taux > 0.02:
                        self.API.marketSell(self.buy_action, self.API.getUserStocks()[self.buy_action])
                        self.buy_price = -1
                        print("Vendre")

        # if(money_left > 1000):
        #     max_to_buy = math.floor(money_left / price)
        #     self.API.marketBuy(first_stonk, max_to_buy)

    def compute_trend(self, values) -> float:
        m = max(values[-1], values[0])
        return (values[-1] / m) - (values[0] / m)

    def get_last_prices(self, action, current_time, window=0) -> list:
        debut = current_time - timedelta(hours=1, minutes=20)
        response = self.API.getPastPrice(action, debut, current_time)
        prices = []
        for time, price in response.items():
            prices.append(price)

        return prices

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