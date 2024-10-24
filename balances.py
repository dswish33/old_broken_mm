from '' import ''
from ws_client_handler import ws_client
from '' import ''

import asyncio
import numpy as np


class bal(object):
    
    def __init__(self, wscli, pairs, rest_client):
        self.wscli = wscli
        self.uri = ""
        self.connection = ""
        self.token = ""
        self.asset_bal = 0
        self.pairs = pairs
        self.rest_client = rest_client
        
    async def initialize(self):
        
        self.token = await self.wscli.get_web_token()
        await self.wscli.connect(url = self.uri, n = self.connection)
        
        balance_msg = balance(token = self.token)
        bal_task = asyncio.create_task(self.wscli.stream_and_send(msg = balance_msg, n = self.connection))
        
    async def process_bals(self):
        
        while True:
            
            if self.wscli.stream['balances']:
                
                i = self.wscli.stream['balances'][0]
                
                if 'type' in i and i['type'] == 'update':
                    
                    asset = self.pairs[0][:-4]
                    
                    if i['data'][0]['asset'] == asset:
                        self.asset_bal = i['data'][0]['balance']
                        self.wscli.stream['balances'].pop(0)
                     
                    else:
                        self.wscli.stream['balances'].pop(0)
                        
                elif 'type' in i and i['type'] == 'snapshot':
                    self.wscli.stream['balances'].pop(0)
                    
                else:
                    print(f"{i}")
                    self.wscli.stream['balances'].pop(0)
            
            else:
                #print("waiting for messages...")
                await asyncio.sleep(3)
                
    
    async def rest_bal(self):
        
        balance = self.rest_client.query_private("Balance")
        
        asset = self.pairs[0][:-4]
    
        bal = balance['result'][asset]
    
        return bal
        

