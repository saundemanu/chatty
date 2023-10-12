import asyncio
import websockets 

connected_clients = {}

async def send_message(websocket, message):
    try:
        await websocket.send(message)
        print(f'sent {message} to {websocket}')
    except websockets.exceptions.ConnectionClosed:
        pass

async def handle_websocket(websocket, path):
    try: 
        # receive passcode and user from client
        data = await websocket.recv()
        passcode, username = data.split('::')
        print(f'Client joined: passcode={passcode}, username={username}')

        if passcode not in connected_clients: 
            connected_clients[passcode] = {}  

        # add client to passcode group with username 
        connected_clients[passcode][username] = websocket
        connect_success = f'You have successfully connected to room {passcode}'
        # Notify the client that they have successfully connected
        await send_message(websocket, connect_success)
        
        # Notify existing clients that a new user has joined
        room_clients = connected_clients.get(passcode, {})
        message_to_existing_clients = f'{username} has joined the room'
        await asyncio.gather(
            *[send_message(client, message_to_existing_clients) for client in room_clients.values() if client != websocket]
        )
        
        while True: 
            message = await websocket.recv()
            print(f'Received message from {username}: {message}')
          
            # broadcast messages to room
            room_clients = connected_clients.get(passcode, {})
            await asyncio.gather(
                *[send_message(client, f'{username}:{message}') for client in room_clients.values() if client != websocket]
            )
    # clean up users who leave / empty rooms
    except websockets.exceptions.ConnectionClosed: 
        for passcode, clients in list(connected_clients.items()):
            if passcode in clients:  # Check if the passcode exists before accessing its clients
                for username, client in list(clients.items()):
                    if websocket == client: 
                        del connected_clients[passcode][username]
                        print(f'Client left: {username}')
                        if not connected_clients[passcode]: 
                            del connected_clients[passcode]
                            print(f'Room {passcode} is empty')


async def main():
    server = await websockets.serve(handle_websocket, 'localhost', 8000)
    print("Server running.")
    await server.wait_closed()

asyncio.run(main())
