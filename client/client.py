import asyncio
import websockets

async def handle_websocket():
    """process websocket connection to server, send and recieve messages"""
    passcode = input("Enter room code: ")
    username = input("Enter username: ")
    async with websockets.connect(f'ws://localhost:8000') as websocket:
        try: 
            await websocket.send(f'{passcode}::{username}')
            
            # Define a function to handle receiving messages
            async def receive():
                while True:
                    message = await websocket.recv()
                    print(f'Received: {message}')
            
            # Create a task to handle receiving messages
            asyncio.create_task(receive())
            while True:
                message = input("Enter a message (or /leave to leave chat):")

                if message == "/leave":
                    break

                await websocket.send(message)

        except websockets.exceptions.ConnectionClosed: 
            print("Connection terminated.")
if __name__ == '__main__':
    asyncio.run(handle_websocket())