from datetime import datetime
import socket
import json
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
import websocket_server

client_list = []
uids_users = dict()
uids = []
active_uids = []
chat_history = []
# def handle_new_client(client, server):
#     print(f"New client connected: {client['address']}")
#     server.send_message(client, "Hello, client!")
#     client_list.append(client)

def handle_client_left(client, server):
    print(f"Client {client['address']} left")
    msg = json.dumps({
        'type':'remove_active_user',
        'data': client_list.index(client)
    })
    for c in client_list:
        if c != client:
            server.send_message(c, msg)
    del active_uids[client_list.index(client)]
    client_list.remove(client)
def handle_client_message(client, server, message):
    print(f"Received message from {client['address'][0]}: {message}")
    data = json.loads(message)
    if data['type'] == 'configure':
        if data['userId'] in uids:
            client_list.append(client)
            active_uids.append(data['userId'])
            chats = json.dumps(chat_history[-10:])
            for i in range(len(uids)):
                if uids[i]==data['userId'] :
                    continue
                else:
                    uid = uids[i]
                    chats = chats.replace(uid, uids_users[uid])
            msg = {
                'type':'chat_history',
                'data': chats,
            }
            server.send_message(client, json.dumps(msg))
            a_users = []
            for a in active_uids:
                a_users.append(uids_users[a])
            msg = json.dumps({
                'type':'active_users',
                'data': a_users,
            })
            server.send_message(client, msg)
            msg = json.dumps({
                'type':'add_active_user',
                'data': uids_users[data['userId']],
            })
            for c in client_list:
                if c != client:
                    server.send_message(c, msg)
    elif data['type'] == 'text' or data['type'] == 'multiFile' or data['type'] == 'singleFile':
        sender = data['sender']
        msg = {
            'timestamp': str(datetime.today()),
            'sender' : uids_users[data['sender']],
            'type': data['type'],
            'data' :data['data']
        }
        for c in client_list:
            if c != client:
                server.send_message(c, json.dumps(msg))
        msg['sender']=sender
        chat_history.append(msg)
    else:
        server.send_close(reason="Unauthorized")
    # Process the message and send a response if needed

server = websocket_server.WebsocketServer(host=IPAddr,port=5005)
# server.set_fn_new_client(handle_new_client)
server.set_fn_message_received(handle_client_message)
server.set_fn_client_left(handle_client_left)

import os 
import sys
if getattr(sys, 'frozen', False):  # Check if running as a frozen executable
        # Get the path to the executable
        executable_path = sys.executable
        # Extract the directory containing the executable
        dir_path= os.path.dirname(executable_path)
else:
    # Running as a regular Python script
    dir_path = os.getcwd()

with open(os.path.join(dir_path, 'resources', 'acc.db'), 'r') as f:
    data = f.read()
    if data:
        accts = [x.split('=') for x in data.split(';')[:-1]]
        for user, pas, seed in accts:
            uids.append(seed)
            uids_users[seed] = user

if __name__ == "__main__":
    server.run_forever()