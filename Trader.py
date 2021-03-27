
import threading
import time
import math
import numpy

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
        
    """Function called at start of run"""
    def run(self):
        
        """You can add initialization code here"""
        
        
        self.t = threading.currentThread()
        while getattr(self.t, "run", True):
            try:
                self.trade()
            except:
                pass
            time.sleep(0)

    """Your trading algorithm goes here!
        The function is called continuously"""
    def trade(self):
        stonks = self.API.getListStocks()
        first_stonk = stonks[0]
        price = self.API.getPrice(first_stonk)
        money_left = self.API.getUserCash()
        if(money_left > 1000):
            max_to_buy = math.floor(money_left / price)
            self.API.marketBuy(first_stonk, max_to_buy)
