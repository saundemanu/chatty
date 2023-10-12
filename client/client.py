import asyncio 
import websockets

async def handle_websocket():
    async with websockets.connect('ws://localhost:8000') as websocket:
       while True:
           message = input("Enter a message (or exit() to leave chat):")
           
           if message == "exit()":
               break
           
           await websocket.send(message)

           response = await websocket.recv()
           print(f'Recieved: {response}')

# Run the asyncio event loop
asyncio.get_event_loop().run_until_complete(handle_websocket())
