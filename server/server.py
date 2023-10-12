import asyncio
import websockets 

connected_clients = set()

async def handle_websocket(websocket, path):
    async for message in websocket:
        #echo message recieved to client
        await websocket.send(message)
        connected_clients.add(websocket)

        try:
            async for message in websocket:
                
                for client in connected_clients: 
                    if client != connected_clients:
                        if client != websocket:
                            await client.send(message)
        finally: 
            connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_websocket, 'localhost', 8000)
    print("Server started")
    await server.wait_closed()

asyncio.run(main())