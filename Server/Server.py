import socket
import threading
import json

import utils
import DataStructures.connections as connections
from DataStructures.connections import Connection
from GameManager import GameManager

from Database.DatabaseManager import DatabaseManager
DB = DatabaseManager()

# change the live and wait system from
# a list to a variable or something with less space.

# list[connection]
live_connections = []

# connections with missed data like username
# for now it's only username
wait_list_connections = []

# server global vars
server: socket.socket = None

# logic global
Game_Manager = GameManager()

# load the config from the config file
config = utils.load_config("config/config.ini")

def main():
    global server

    try:
        # create the server socket
        server = socket.socket()

        IP = config["SOCKET"]["SERVER_ADDRESS"]
        PORT = int(config["SOCKET"]["SERVER_PORT"])

        server.bind((IP, PORT))
        server.listen(int(config["SOCKET"]["MAX_USERS"]))

        utils.server_print("The server is online on: " + IP + "/" + str(PORT))

        # load users into the server
        while True:
            client_socket, client_address = server.accept()
            con = Connection(client_address, client_socket)

            # check if there is a connection from the same computer
            # a multi connections from the same computer is not allow!
            if client_address in [c.data['address'] for c in live_connections] + [c.data['address'] for c in
                                                                                  wait_list_connections]:
                client_socket.close()
            else:
                wait_list_connections.append(con)
                thread = threading.Thread(target=handle_client, args=[con])
                thread.start()

    except Exception as e:
        utils.server_print(str(e))
    finally:
        print("Server is close!")


def handle_client(con: Connection):
    try:
        # send the client that the connection has been successful.
        # response (json) format: {code: int, event: string, msg?: string, data?: object}
        con.connection.send(json.dumps({'event': 'connection_initialized'}).encode())
        utils.server_print("A new connection has been initialized, " + str(con.data))

        while True:
            request = json.loads(con.connection.recv(1024).decode())

            if 'event' not in request.keys():
                con.connection.send(json.dumps({'code': 400, 'event': 'bad request'}).encode())
                continue

            # authorization check
            if 'username' not in con.data.keys():
                if request['event'] == 'login':
                    if 'data' not in request.keys() or 'username' not in request['data'].keys() or 'password' not in request['data'].keys():
                        con.connection.send(json.dumps({'code': 400, 'event': 'bad request', "msg": "'data' is required for login request."}).encode())
                        continue

                    if not DatabaseManager.verify_user_data(request['data']['username'], request['data']['password']):
                        con.connection.send(json.dumps({'code': 406, 'event': 'login error', "msg": "the username or password is incorrect"}).encode())
                        continue

                    live_connections.append(con)
                    wait_list_connections.remove(con)
                    con.status = connections.Status.Live
                    con.data["username"] = request['data']['username']

                    con.connection.send(json.dumps({'code': 200, 'event': 'login complete', "msg": "the login was successful", 'data': {}}).encode())

                elif request['event'] == 'register':
                    if 'data' not in request.keys() or 'username' not in request['data'].keys() or 'password' not in request['data'].keys():
                        con.connection.send(json.dumps({'code': 400, 'event': 'bad request', "msg": "'data' is required for register request."}).encode())
                        continue

                    if DatabaseManager.is_exists("users", request['data']['username']):
                        con.connection.send(json.dumps({'code': 406, 'event': 'username error', "msg": "username is already exists."}).encode())
                        continue

                    DB.add_data("users", request['data']['username'], {"password": DatabaseManager.hash(request['data']['password'])})
                    con.connection.send(json.dumps({'code': 200, 'event': 'register complete', "msg": "the register was successful"}).encode())
            else:
                if request['event'] == 'logout':
                    if 'username' not in con.data.keys():
                        con.connection.send(json.dumps({'code': 401, 'event': 'unauthorized', "msg": "login before trying to logout."}).encode())
                        continue

                    wait_list_connections.append(con)
                    live_connections.remove(con)
                    con.status = connections.Status.Wait
                    con.data.pop("username")

                    con.connection.send(json.dumps({'code': 200, 'event': 'logout complete', "msg": "the logout was successful"}).encode())

                if request['event'] == 'start_queue':
                    con.status = connections.Status.Queue
                    Game_Manager.add_to_queue(con)
                    con.connection.send(json.dumps({'code': 200, 'event': 'queue stated', "msg": "please wait in queue until we find a match for you."}).encode())
                if request['event'] == 'stop_queue':
                    con.status = connections.Status.Live
                    Game_Manager.remove_from_queue(con)
                    con.connection.send(json.dumps({'code': 200, 'event': 'queue stopped', "msg": "queue closed."}).encode())

                if request['event'] == "start_game" and con.status == con.status.InGame:
                    pass

                if request['event'] == "do_move" and con.status == connections.Status.InGame:
                    pass

    except Exception as e:
        utils.server_print(str(e))
    finally:
        # remove the connection from the connection list
        if con.status == connections.Status.Wait:
            wait_list_connections.remove(con)
        elif con.status == connections.Status.Live:
            live_connections.remove(con)
        elif con.status == connections.Status.Queue:
            Game_Manager.remove_from_queue(con)
            utils.server_print(con.data["address"].__str__() + " Removed from queue.")

        utils.server_print("A connection with a client closed, " + str(con.data))
        con.connection.detach()
        con.connection.close()


if __name__ == '__main__':
    main()
