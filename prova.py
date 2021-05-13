# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:18:36 2021

@author: ricca
"""
import pandas as pd
import numpy as np 
from scipy import stats

np.random.seed(42)   
percentile_samples = np.random.pareto(1.36, 100000)
normal = np.random.normal(50, 15, 100000)

class Agent(object):
    def __init__(self, agent_id): #devo aggiungere le altre classi tra le parentesi per accedere alle variabili? Viene creata un instance per ogni stock?
        self.agent_id = agent_id
 #       self.Seed = np.random.seed(agent_id)
        self.Resources = np.random.pareto(1.36) ### totale risorse? 
        self.percentile_of_resources = stats.percentileofscore(percentile_samples, self.Resources) #devo aggiungere del "rumore"
        self.Hindsight = np.random.normal(loc=50, scale=20)
        self.Trendsight = np.random.normal(loc=50, scale=20)
        self.Greediness =  np.percentile(normal, self.percentile_of_resources)
        self.Information_Sensibility = np.random.normal(loc=50, scale=20)
        self.Influence = 0 
        self.Influence_Sensibility = 0   
###Non sapendo quale parametro tra influence e influence sensibility scegliere
###ho messo entrambi.
        
### Come mi connetto ad altri agenti? Lista di tuple? Dizionario? Devo fare qualcosa che prenda le risorse degli altri agenti e assegni
### in proporzione alle risorse un certo numero di agenti. Potrei fare un'altra classe? 
       # self.change = 

    def print_res(self):
      print(self.Resources)
      print(self.percentile_of_resources)
      print(self.Greediness)
      print(self.Information_Sensibility)  
      
    def check_news(self):
        #forse posso creare una lista unica da tutte le stock e checkare quella? cosí mi sembra
        #di dover creare una instance agente per ogni stock. 
        pass
    
    def change(self):   #vettore che mi indica di quanto modificare hindisght,trendsight...
        pass


class Model(object):
    def __init__(self):
        self.agent_set = []
        
    def create_agent_set(self, agent_num):
        for i in range(agent_num):
            self.agent_set.append(Agent(i))      #agent_set[i].parametro
    
    def last_tick_price(self, stock_type):
        return -1

    
agent_try = Agent(500)

agent_try.print_res()

my_model = Model()
my_model.create_agent_set(10)

# b = np.random.pareto(1.36)
# print(b)



class Stock(object):
    def __init__(self, stock_type, true_value):
        self.stock_type = stock_type
        self.true_value = true_value
        self.news = 0
        self.last_avg_price = true_value
    
    def last_price(self):
        self.last_avg_price = my_model.last_tick_price(self.stock_type)
    
    def update_news(self):
       # self.news = (self.true_value - self.last_avg_price)/(self.true_value + self.last_avg_price)
        pass
    
    # def record_avg_price(self):
    #     self.avg_prices_records = []
    #     self.avg_prices_records.append(self.last_price)
    
    
my_stock = Stock(4, 120)

my_stock.last_price()
