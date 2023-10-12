import asyncio
import websockets

async def gather_user_input():
    passcode = await asyncio.to_thread(input, "Enter room code: ")
    username = await asyncio.to_thread(input, "Enter username: ")
    return passcode, username

async def handle_websocket():
    passcode, username = await gather_user_input()

    async with websockets.connect(f'ws://localhost:8007') as websocket:
        try:
            await websocket.send(f'{passcode}::{username}')
            
            # Wait for connection verification
            verification = await websocket.recv()
            print(f'{verification}')

            async def receive():
                while True:
                    message = await websocket.recv()
                    print(f'{message}')

            asyncio.create_task(receive())

            while True:
                message = await asyncio.to_thread(input, "Enter a message (or /leave to leave chat): ")

                if message == "/leave":
                    break

                await websocket.send(message)

        except websockets.exceptions.ConnectionClosed: 
            print("Connection terminated.")

if __name__ == '__main__':
    asyncio.run(handle_websocket())
