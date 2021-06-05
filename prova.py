# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:18:36 2021

@author: ricca
"""
import pandas as pd
import numpy as np 
from scipy import stats 
from random import randint, uniform
import networkx as nx
import matplotlib.pyplot as plt
np.random.seed(42)   
percentile_samples = np.random.pareto(1.36, 100000)
normal = np.random.normal(50, 20, 100000)
greediness_threshold = 0.15
class Agent(object):
    def __init__(self, agent_id): #devo aggiungere le altre classi tra le parentesi per accedere alle variabili? Viene creata un instance per ogni stock?
        self.agent_id = agent_id
        self.Resources = np.random.pareto(1.36)*10000 ### totale risorse? 
        self.percentile_of_resources = stats.percentileofscore(percentile_samples, self.Resources/10000) #devo aggiungere del "rumore"
        self.Truesight = np.random.choice(normal)/np.max(normal) #stessa cosa di greediness ma con distribuzione normale
        self.Trendsight = np.random.choice(normal)/np.max(normal)
        self.Greediness =  np.percentile(normal, self.percentile_of_resources)/np.max(normal)
        self.Information_Sensibility = abs(np.random.choice(normal)/np.max(normal))
       #self.Influence = 0 
        self.Influence_Sensibility = 0   
        self.change_vector = [0,0,0,0]
        self.portfolio = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self.Resources_last_tick = 0
        self.Market_Involvement = 0
        
  

### Come mi connetto ad altri agenti? Lista di tuple? Dizionario? Devo fare qualcosa che prenda le risorse degli altri agenti e assegni
### in proporzione alle risorse un certo numero di agenti. Potrei fare un'altra classe? 
        

    def print_res(self):
      print(self.Resources)
      print(self.percentile_of_resources)
      print(self.Greediness)
      print(self.Information_Sensibility)  
      
      
    def __repr__(self):
        rep = 'Agent(' + str(self.agent_id) + ',' +  str(self.percentile_of_resources) + ')' 
        return rep

        

    def truesight_mapping(self):
        self.truesight_price = []
        for i in range(10):
            self.truesight_price.append(np.random.normal(loc=Stock(i).true_value, scale=(1-self.Truesight)*(Stock(i).true_value/10)))
        
    def trendsight_mapping(self):
        self.trendsight_price = []
        for i in range(10):
            self.trendsight_price.append((0.40*Stock(i).last_avg_price    
                                        + 0.25*Stock(i).two_avg_price
                                        +0.15*Stock(i).three_avg_price
                                        +0.1*Stock(i).four_avg_price
                                        +0.1*Stock(i).five_avg_price))
 ###fare list pesi invece che 0.4...
 
    def tot_price_mapping(self):
        self.tot_price = []
        for i in range(10):
            self.tot_price.append((self.truesight_price[i] * self.Truesight + self.trendsight_price[i]*self.Trendsight)/(self.Truesight + self.Trendsight))
    


class Model(object):
    def __init__(self):
        self.agent_set = []
        self.agent_set_in_market = []
        self.stock_set = []
        self.list_of_dict = []
        
        
        

    
    def create_global_portfolio(self, global_portfolio):
        self.global_portfolio = global_portfolio
        
        
    def create_agent_set(self, agent_num):
        for i in range(agent_num):
            self.agent_set.append(Agent(i))      #agent_set[i].parametro
            
    def char_df_creation(self):
        self.list_of_dict.clear()
        for agent in self.agent_set:
            self.char_dict = {'Resources':agent.Resources,
                          'Truesight':agent.Truesight,
                          'Trendsight':agent.Trendsight,
                          'Greediness':agent.Greediness,
                          'Info Sensibility':agent.Information_Sensibility,
                          'Influence Sensibility':agent.Influence_Sensibility}
            self.list_of_dict.append(self.char_dict) 
        self.char_df = pd.DataFrame(self.list_of_dict,  index=self.agent_set)
            
    def create_stock_set(self, stock_num):
        for i in range(stock_num):
            self.stock_set.append(Stock(i))
            
    def divide_portfolio(self):
        self.sum_of_percentiles = 0
        self.percent_vector = np.array([])
        for a in self.agent_set:
            if a.percentile_of_resources > 35:
                self.sum_of_percentiles += a.percentile_of_resources
        self.divided_portfolio = self.global_portfolio / self.sum_of_percentiles
        
        
        

    
    def distribute_stocks(self):
        for i in self.agent_set:
            if i.percentile_of_resources > 35:
                for j in range(len(self.stock_set)):
                    i.portfolio[j] = int(self.divided_portfolio[j] * i.percentile_of_resources)
    
    
    
    
    
    
    
    def network_creation(self):
        self.agent_set_ordered_by_res =  sorted(self.agent_set, key=lambda x: x.percentile_of_resources, reverse=True)
        self.nodes_sorted_by_degree = []
       
        
  
        
        self.network = nx.barabasi_albert_graph(10, 2)
        self.sorted_nodes_degree_tuples =  sorted(self.network.degree, key=lambda x: x[1], reverse=True)
        for i in self.sorted_nodes_degree_tuples:
            self.nodes_sorted_by_degree.append(i[0])

        for i in range(len(self.nodes_sorted_by_degree)):
            self.network.nodes[self.nodes_sorted_by_degree[i]]['Agent_ID'] = self.agent_set_ordered_by_res[i]
        
        
        labels = nx.get_node_attributes(self.network, 'Agent_ID') 
        nx.draw(self.network,labels=labels,node_size=1000)
    # def check_who_has_money(self):
    #     for i in self.agent_set:
    #         if i.percentile_of_resources > 35:
    #             print('yes')
    #         else:
    #             print('no')
    
    def create_agent_set_in_market(self):
        for element in self.agent_set:
            if element.Greediness > greediness_threshold:
                self.agent_set_in_market.append(element)

    
    def market_involvement(self):
        for element in self.agent_set_in_market:
            element.Market_Involvement = stats.percentileofscore(normal, element.Greediness*100)/50
    
    
    
    def news_signal(self):
        for stock in self.stock_set:
            if stock.true_value > stock.last_avg_price:
                stock.news = 100 - (stock.last_avg_price / stock.true_value)
            else:
                stock.news = (stock.true_value / stock.last_avg_price) - 100
                
                

        
                

    # def price_mapping(self):
    #     self.prices_array = np.zeros((len(self.agent_set_in_market), len(self.stock_set)))
    #     for i in range(len(self.agent_set_in_market)):
    #         for j in range(len(self.stock_set)):
    #             self.prices_array[i][j] = ((self.agent_set_in_market[i].Trendsight * self.stock_set[j].last_avg_price + self.agent_set_in_market[i].Truesight * self.stock_set[j].true_value)/100)*(1 + self.agent_set_in_market[i].Greediness/100)
    #     self.dataframe_prices = pd.DataFrame(data=self.prices_array,index=self.agent_set_in_market, columns=self.stock_set )
        

    
    # def buy_sell_mapping(self):
    #     self.buy_sell_ranking = np.zeros((len(self.agent_set_in_market), len(self.stock_set)))
    #     for i in range(len(self.agent_set_in_market)):
    #         for j in range(len(self.stock_set)):
    #             self.buy_sell_ranking[i][j] = ((self.agent_set_in_market[i].Trendsight * self.stock_set[j].last_avg_price + self.agent_set_in_market[i].Truesight * self.stock_set[j].true_value)/100)*(1 + self.agent_set_in_market[i].Greediness/100) + self.stock_set[j].news 
    #     self.dataframe_stock = pd.DataFrame(data=self.buy_sell_ranking,index=self.agent_set_in_market, columns=self.stock_set)
        
        # self.dataframe_stock.values.sort()
        
        # self.dataframe_stock = self.dataframe_stock.iloc[:,::-1]
      
        # self.stock_ranking = self.dataframe_stock.values
        # self.stock_ranking.sort(axis=1)
        # self.stock_ranking = self.stock_ranking[:,::-1]
        

    

    # def exchange(self):
    #     for agent in self.agent_set_in_market:
            
            
                        
     
    
            

    
    
    def last_tick_price(self, stock_type):
        return -1
    

    


    def update_change_vectors(self):
        for i in self.agent_set:
            if i.Resources > i.Resources_last_tick:
                for j in i.change_vector:
                    j -= 0.1
            else:
                i.change_vector[randint(0,3)] = (i.Resources - i.Resources_last_tick) ###ERROR:'tuple' object does not support item assignment
                



class Stock(object):
    def __init__(self, stock_type):
        self.stock_type = stock_type
        self.true_value = 1000              #uniform(10.0, 250.0)
        self.news = 0
        self.last_avg_price = self.true_value
        self.two_avg_price = self.true_value
        self.three_avg_price = self.true_value
        self.four_avg_price = self.true_value
        self.five_avg_price = self.true_value
        
        
    def __repr__(self):
        rep = 'Stock(' + str(self.stock_type) + ',' +  str(self.true_value) + ')' 
        return rep
    
    def last_price(self):
        self.last_avg_price = my_model.last_tick_price(self.stock_type)
    
    def update_news(self):
       # self.news = (self.true_value - self.last_avg_price)/(self.true_value + self.last_avg_price)
        pass
    
    # def record_avg_price(self):
    #     self.avg_prices_records = []
    #     self.avg_prices_records.append(self.last_price)


#repr

class Book(object):
    def __init__(self):
        self.orders = []
        
    def add_order(self, order):
        self.orders.append(order)
        
    def clearing(self):
        buy_order = []
        sell_order = []
        for i in range(len(self.orders)):
            for j in range(len(self.orders)):
                if self.orders[i][0] != self.orders[j][0] and self.orders[i][0] != 'None' and self.orders[j][0] != 'None':
                    if self.orders[i][4] != self.orders[j][4]:
                        if self.orders[i][1] == self.orders[j][1]:
                            if self.orders[i][0] == 'Buy':
                                buy_order = (self.orders[i])
                                sell_order = (self.orders[j])
                                if sell_order[2] > buy_order[2]:
                                    sell_order[4].portfolio[sell_order[1]] -= buy_order[2]
                                    buy_order[4].portfolio[buy_order[1]] += buy_order[2]
                                    self.orders[j][2] -= buy_order[2] 
                                    self.orders.append(self.orders.pop(self.orders.index(self.orders[j])))
                                    self.orders[i] = ['None', 0,0, 0,'None']
                                elif buy_order[2] > sell_order[2]:
                                    sell_order[4].portfolio[sell_order[1]] -= sell_order[2]
                                    buy_order[4].portfolio[buy_order[1]] += sell_order[2]
                                    self.orders[i][2] -= sell_order[2] 
                                    self.orders.append(self.orders.pop(self.orders.index(self.orders[i])))
                                    self.orders[j] = ['None', 0,0, 0,'None']
                            else:
                                sell_order = (self.orders[i])
                                buy_order = (self.orders[j])
                                if sell_order[3] <= buy_order[3] and buy_order[4].Resources >= buy_order[3]: #devo far si che chi compra abbia abbastanza soldi per tutte le azioni --> avviene prima, nel momento di fare l'ordine
                                    sell_order[4].Resources += buy_order[3]
                                    buy_order[4].Resources -= buy_order[3]
                                    if sell_order[2] > buy_order[2]:
                                        sell_order[4].portfolio[sell_order[1]] -= buy_order[2]
                                        buy_order[4].portfolio[buy_order[1]] += buy_order[2]
                                        self.orders[i][2] -= buy_order[2] 
                                        self.orders.append(self.orders.pop(self.orders.index(self.orders[i])))
                                        self.orders[j] = ['None', 0,0, 0,'None']
                                    elif buy_order[2] > sell_order[2]:
                                        sell_order[4].portfolio[sell_order[1]] -= sell_order[2]
                                        buy_order[4].portfolio[buy_order[1]] += sell_order[2]
                                        self.orders[j][2] -= sell_order[2] 
                                        self.orders.append(self.orders.pop(self.orders.index(self.orders[j])))
                                        self.orders[i] = ['None', 0,0, 0,'None']
                                
                                ## scambio se ho i soldi o la stock prima della sparizione dell'ordine per farlo scadere aggiungi elemento lista tick 
    def clear_orders(self):
        for order in (self.orders):   
            if order[0] == 'None':
                self.orders.remove(order)
                Book.clear_orders(self)           
                
                    

















#g_p = {1:10,
#        2:200,
#        3:100,
#        4:500,
#        5:120,
#        6:800,
#        7:40,
#        8:50,
#        9:1100,
#        10:500}







my_model = Model()
my_book = Book()
my_model.create_agent_set(10)
my_model.create_agent_set_in_market()
my_model.create_stock_set(10)
my_stock = Stock(4)
my_model.market_involvement()
my_stock.last_price()
g_p = np.array([1000, 100, 2000, 5000, 7000, 111000, 1000, 16000, 11000, 541000])
my_model.create_global_portfolio(g_p)   
my_model.divide_portfolio()                             
my_model.distribute_stocks()
#my_model.check_who_has_money()
my_model.network_creation()

# for i in my_model.agent_set_in_market:
#     print(i.Market_Involvement)
    

    
my_model.agent_set[0].truesight_mapping()
my_model.agent_set[0].trendsight_mapping()
my_model.agent_set[0].tot_price_mapping()

dummy_price = [['Sell', 0, 5, 999],
               ['Buy', 0, 10, 1000],
               ['Buy', 0, 20,1000],
               ['Sell', 0, 15,1000],
               ['Buy', 0, 5, 10],
               ['Sell', 0, 100, 1001],
               ['Buy', 0, 25, 1002],
               ['Buy', 0, 10, 1000]]
j = 0
for i in my_model.agent_set_in_market:
    a = []
    a.append(dummy_price[j][0]) #compro o vendo 
    a.append(dummy_price[j][1]) #quale stock
    a.append(dummy_price[j][2])  #quante stock 
    a.append(dummy_price[j][3])#a che prezzo
    a.append(i) #agente
    my_book.add_order(a)
    j += 1



#my_book.clearing()