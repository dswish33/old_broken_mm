#!/usr/bin/env python
# coding: utf-8


from '' import ''
from ws_client_handler import ws_client
from '' import ''

import asyncio
import numpy as np


class ordrbk(object):
    
    def __init__(self, wscli, depth, pairs):
        self.wscli = wscli
        self.uri = ""
        self.connection = ""
        self.bids = []
        self.asks = []
        self.depth = depth
        self.pairs = pairs
   
        
    async def initialize(self):
         
        await self.wscli.connect(url = self.uri, n = self.connection)
        
        book_msg = ob(pairs = self.pairs, depth = self.depth, snapshot = True)
        book_task = asyncio.create_task(self.wscli.stream_and_send(msg = book_msg, n = self.connection))
        
        
    async def process_book(self):
    
        while True:
            
            if self.wscli.stream['book']:
               
                i = self.wscli.stream['book'][0]
            
                if 'type' in i and i['type'] == 'snapshot':
                    
                    for h in i['data'][0]['bids']:
                        price, qty = h['price'], h['qty']
                        self.bids.append((price, qty))
                
                    for m in i['data'][0]['asks']:
                        price, qty = m['price'], m['qty']
                        self.asks.append((price, qty))
                        
                    print(f"bids: {self.bids}")
                    print(f"asks: {self.asks}")
                    self.wscli.stream['book'].pop(0)
                    
                    
                elif 'type' in i and i['type'] == 'update':
                
                    if i['data'][0]['bids']:
                        
                        for h in i['data'][0]['bids']:
                            
                            price, qty = h['price'], h['qty']
                        
                            indx = len(self.bids) - 1
                            while indx >= 0:
                                if self.bids[indx][0] == price:
                                    self.bids.pop(indx)
                                    break
                                indx -= 1
                        
                            if qty != 0:
                                self.bids.append((price, qty))
                            else:
                                pass
                    else:
                        pass
                    
                    if i['data'][0]['asks']:
                        
                        for m in i['data'][0]['asks']:
                            
                            price, qty = m['price'], m['qty']
                            
                            indx = len(self.asks) - 1
                            while indx >= 0:
                                if self.asks[indx][0] == price:
                                    self.asks.pop(indx)
                                    break
                                indx -= 1
                                      
                            if qty != 0:
                                self.asks.append((price, qty)) 
                            else:
                                pass
                    else:
                        pass 
                    
                    await self.update_book()
                    self.wscli.stream['book'].pop(0)
                    
                else:
                    print(f"{i}")
                    self.wscli.stream['book'].pop(0)
   
            else:
                #print("waiting for messages...")
                await asyncio.sleep(3)
            
            
    async def update_book(self):
        
        sorted_bids = sorted(self.bids, key = lambda x: x[0], reverse = True)
        self.bids = sorted_bids[0:self.depth]
        
        sorted_asks = sorted(self.asks, key = lambda x: x[0], reverse = False)
        self.asks = sorted_asks[0:self.depth]
        
        
        
        
      
        
        
    

