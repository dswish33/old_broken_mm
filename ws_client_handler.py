from "" import API
import websockets
import asyncio
import orjson
import numpy as np


class ws_client(object):
    
    def __init__(self, client):
        self.client = client
        self.websocket = {}
        self.stream = {
            "book" : [],
            "trade" : [],
            "executions" : [],
            "balances" : []
        }
        self.lock = asyncio.Lock()
        

    async def get_web_token(self):
    
        token = self.client.query_private("GetWebSocketsToken")['result']['token']
        
        return token


    async def connect(self, url, n):
        self.websocket[n] = await websockets.connect(url)
        print(f"Connected to {url}")
    
    
    async def stream_and_send(self, msg, n):
        ws = self.websocket.get(n)
            
        if ws:
            
            try: 
                
                data = orjson.dumps(msg)
                
                await ws.send(data)
                
                async for message in ws:
                    
                    r = orjson.loads(message)
                    c = r.get("channel")
                    
                    async with self.lock:
                        if c in self.stream:
                            self.stream[c].append(r)
                
            #except websockets.ConnectionClosed:
                #continue

            except Exception as e:
                print(f"Error with feed: {e}")
                print(f"{msg}")
                raise e 
                
    async def close_connection(self, n):
        ws = self.websocket.get(n)
        
        await ws.close()
        
        print("Connection closed")
        
            