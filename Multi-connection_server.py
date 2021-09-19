import base64
import codecs
import socket
import threading
import ast
import time
import random

PORT = 5050
SERVER = "25.70.218.163"  # socket.gethostbyname(socket.gethostname())  # 192.168.178.119 #192.168.178.101 #25.70.218.163
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNESSO"
TEST_MSG = "!TEST"
INFO_MSG_T1 = "!INFO_T1"
INFO_MSG_T2 = "!INFO_T2"
CHAT_ROOMS_MSG_T1 = "!CHAT_ROOMS_T1"
CHAT_ROOMS_MSG_T2 = "!CHAT_ROOMS_T2"
NAME_MSG = "!NOME"
REPLACE_MSG = "!RIMPIAZZA"
RECONN_MSG = "!RICONNETTI"
IP_MSG = "!IP"
CREATED_ROOM = "!STANZACREATA"
PASS_MSG = "!PASS"
NORMAL_MESSAGE = "!N_MSG"
LONG_MESSAGE = "!L_MSG"
END_LONG_MESSAGE = "!F_L_MSG"
TO_JOIN_MSG = "!PERUNIRSI"
NEW_CLIENT_MSG = "!NUOVOCLIENT"
JOINED = "!UNITO"
RECV_MSG = "!RICEVUTO"
LEFT_CLIENT_MSG = "!USCITO"
REMOVE_CLIENTS_TO_CHAT = "!RIMUOVI"
MESSAGE = "!MESSAGGIO"
ALPHABET_MSG = "!ALFABETO"
ERROR_MSG = "!ERRORE_RICEZIONE"
HEADER = 3
server = socket.socket()
server.bind(ADDR)
ENCODE_ALPHABET = {}
DECODE_ALPHABET = {}
clients = []
globals()[RECV_MSG] = {}
send_message_counter = 0
char_long = 256
min_byte_char_random = 1
max_byte_char_random = 2
min_padding_sx_n = 1
max_padding_sx_n = 2
min_padding_dx_n = 1
max_padding_dx_n = 2
messages_to_send = {"": ""}
recv_bool_block = False

def create_token_by_alphabet(alphabet):
    all_chars = ""
    for i in range(char_long):
        all_chars += (chr(i))
    token = ""
    for char in all_chars:
        token += alphabet[char]
    print(token)
    return token


def last_encode(alf, encription_level):
    r = ""
    for i in range(encription_level):
        r = str(str(alf).encode(FORMAT))
        r = r[2:len(r) - 1].encode("ascii")
        r = base64.b64encode(r)
    r = str(r)
    r = r[2:len(r) - 1]
    r = r.encode("utf-16")
    return r


def encode(string, alphabet_=()):
    try:
        if alphabet_ == ():
            if isinstance(string, str):
                return string.encode(FORMAT)
            else:
                return string
    except IndexError:
        return string.encode(FORMAT)
    string_encoded = ""
    for char in string:
        string_encoded += alphabet_[1][char]
    return last_encode(string_encoded, alphabet_[2])


def get_key(alf, val):
    for key, value in alf.items():
        if val == value:
            return key

    return "key doesn't exist"


def send_to_client(client_, msg):
    message = msg
    msg_lenght = len(message)
    send_length = str(msg_lenght).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    if str(type(client_)) == "<class 'socket.socket'>":
        print(
            f"\n\nInvio il messaggio all'indirizzo:   {client_.getpeername()}\nMessaggio da inviare </{msg}/>\nLunghezza del messaggio da inviare {send_length}")
        client_.send(send_length)
        client_.send(message)
    else:
        client = None
        for client_connected in clients_connected:
            if client_connected.getpeername()[0] == client_:
                client = client_connected
        if client is not None:
            print(
                f"\n\nInvio il messaggio all'indirizzo:   {client.getpeername()}\nMessaggio da inviare </{msg}/>\nLunghezza del messaggio da inviare {send_length}")
            client.send(send_length)
            client.send(message)


def send_long_message_to_client(client, msg):
    piece_msg = "9"
    header_str = ""
    for i in range(HEADER):
        header_str += "9"
        piece_msg += "9"
    while len(piece_msg) > HEADER:
        piece_msg = msg[:int(header_str)]
        msg = msg[int(header_str):]
        if len(piece_msg) != 0:
            print(f"LONG coso: {encode(LONG_MESSAGE)}")
            send_to_client(client, encode(LONG_MESSAGE))
            print(f"piece_msg coso: {piece_msg}")
            send_to_client(client, piece_msg)
        print(f"While esterno: {len(piece_msg)}")
        while True:
            # ricezione RECV_MSG
            msg_recv = globals()[client.getpeername()[0]+"_recv"] if not globals()[client.getpeername()[0] + "_without_alph"] else recv(client)
            print(f"recv__msg: {msg_recv}")
            print(f"len(piece_msg): {len(piece_msg)}")
            print(f"HEADER: {HEADER}")
            if msg_recv is not None or len(piece_msg) < int(header_str):
                globals()[client.getpeername()[0]+"_recv"] = None
                break
            time.sleep(0.05)
    send_to_client(client, encode(END_LONG_MESSAGE))


def send_message_to_server_with_check(client, msg, alphabet_=(), direct=False):
    print(f"alphabet_: {alphabet_}")
    msg_n = msg
    msg = encode(msg, alphabet_)
    print(f"Msg: {msg_n}\nMsg encoded: {msg}")
    if len(str(len(msg))) <= HEADER:
        send_to_client(client, encode(NORMAL_MESSAGE))
        send_to_client(client, msg)
    else:
        send_long_message_to_client(client, msg)


def store_message(client, message_type_long, msg, direct):
    global recv_bool_block
    if not any([True if client == conn else False for conn in messages_to_send.keys()]):
        print("testtt ehehe")
        messages_to_send.update({client: []})
    print(f"recv_bool: {recv_bool_block}")
    if not recv_bool_block or direct:  # not recv_bool_block or direct
        print("INVIO MESSAGGIO")
        if not direct:
            recv_bool_block = True
        send_to_client(client, message_type_long)
        if not message_type_long == END_LONG_MESSAGE.encode(FORMAT):
            send_to_client(client, msg)
    else:
        print("SALVATAGGIO MESSAGGIO")
        messages_to_send[client].append([message_type_long, msg])
    print(messages_to_send)
    if not direct:
        if messages_to_send[client][0][0] == END_LONG_MESSAGE.encode(FORMAT):
            recv_bool_block = False


def send_message_to_client(conn):
    global messages_to_send, recv_bool_block
    if messages_to_send[conn]:
        print(f"COSO INIZIALE: {messages_to_send[conn]}")
        send_to_client(conn, messages_to_send[conn][0][0])
        if not messages_to_send[conn][0][0] == END_LONG_MESSAGE.encode(FORMAT):
            send_to_client(conn, messages_to_send[conn][0][1])
        del messages_to_send[conn][0]
        print(f"COSO FINAALE: {messages_to_send[conn]}")
    else:
        recv_bool_block = False


def recv(client, decode=False):
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length.strip())
        msg = client.recv(msg_length)
        print("\nDimensione del messaggio ricevuto:")
        print(f"Corretta") if msg_length == len(msg) else print(
            f"Errata\nDimensione del messaggio da ricevere: {msg_length}\nDimensione del messaggio effettivo: {len(msg)}")
        print(
            f"\n\nRicezione da:   {client.getpeername()}\nLunghezza del messaggio da ricevere {msg_length}\nMessaggio da ricevere </{msg}/>")
        return msg if not decode else msg.decode(FORMAT)
    else:
        print(f"\n\nErrore di ricezione da:   {client.getpeername()}\nMessaggio da ricevere {msg_length}")
        return ERROR_MSG


def get_clients_to_chat(ip):
    room_ips = []
    clients_to_chat = []
    for room in chat_rooms:
        if ip in room[2]:
            room_ips = room[2]
    for client in clients_connected:
        for ip_in_chat in room_ips:
            if ip_in_chat == client.getpeername()[0] and not ip_in_chat == ip:
                clients_to_chat.append(client)
    return clients_to_chat


def first_decode(bytes, encription_level):
    s = bytes.decode("utf-16")
    s = s.encode('raw_unicode_escape')
    s, _ = codecs.escape_decode(s, 'hex')
    for i in range(encription_level):
        s = base64.b64decode(s)
        s = s.decode("ascii")
        s = s.encode('raw_unicode_escape')
        s, _ = codecs.escape_decode(s, 'hex')
        s = s.decode("utf-8")
    return s


def decode(byte, alf):
    try:
        return byte.decode(FORMAT)
    except UnicodeError:
        str_ = first_decode(byte, alf[2])
        re = ""
        for n in range(int(len(str_) / alf[0])):
            re += alf[1][str_[alf[0] * n:alf[0] * n + alf[0]]]
        return re


def recv_with_long(conn, alf=(), type=None):
    message_type_long = recv(conn, decode=True)
    msg = b""
    print(f"TIPO MESSAGGIO: {message_type_long}")
    if message_type_long == NORMAL_MESSAGE:
        msg = recv(conn)
    elif message_type_long == LONG_MESSAGE:
        msg += recv(conn)
        while True:
            send_message_to_server_with_check(conn, RECV_MSG)
            message_type_long = recv(conn, decode=True)
            if message_type_long == END_LONG_MESSAGE:
                break
            msg += recv(conn)
    return (
        decode(msg, alf) if alf != () else msg) if not message_type_long == ERROR_MSG else ERROR_MSG


def handle_client(conn, addr):
    global clients_connected, ENCODE_ALPHABET, DECODE_ALPHABET
    print(f"\n[NUOVA CONNESSIONE] \n---> {addr} connesso\n")
    created_room = False
    connected = True
    print("\n")
    msg = recv(conn)
    if msg == TEST_MSG.encode(FORMAT):
        client_already_connected = False
        for client in clients:
            if client[0] == addr[0]:
                client_already_connected = True
                break
        if not created_room:
            send_to_client(conn, str(client_already_connected).encode(FORMAT))
        connected = False
    if connected:
        globals()[addr[0] + "_without_alph"] = True
        globals()[RECV_MSG].update({conn: None})
        all_chars = ""
        for i in range(char_long):
            all_chars += (chr(i))
        new_alphabet_encode = {}
        random_seed = None
        seed = int(round(time.time() * 1000)) if random_seed is None else random_seed
        random.seed(seed)
        byte_char = random.randint(min_byte_char_random, max_byte_char_random)
        encription_level = 1  # random.randint(1, 2)
        for n, char in enumerate(all_chars):
            while True:
                new_char = ""
                for i in range(byte_char):
                    new_char += all_chars[random.randint(0, len(all_chars) - 1)]
                if new_char not in new_alphabet_encode.values():
                    new_alphabet_encode.update({char: new_char})
                    break
        if not addr[0] in ENCODE_ALPHABET:
            ENCODE_ALPHABET.update({addr[0]: {0: byte_char, 1: new_alphabet_encode, 2: encription_level}})
        else:
            ENCODE_ALPHABET[addr[0]] = {0: byte_char, 1: new_alphabet_encode, 2: encription_level}
        print(f"Seme generazione: {seed}")
        new_alphabet_encode_msg = (create_token_by_alphabet(new_alphabet_encode))
        padding_sx_n = random.randint(min_padding_sx_n, max_padding_sx_n)
        padding_dx_n = random.randint(min_padding_dx_n, max_padding_dx_n)
        print(f"padding_sx_n: {padding_sx_n}")
        print(f"padding_dx_n: {padding_dx_n}")
        print(f"byte_char: {byte_char}")
        print(f"encription_level: {encription_level}")
        temp = ""
        for i in range(padding_sx_n):
            temp += all_chars[random.randint(0, len(all_chars) - 1)]
        temp += new_alphabet_encode_msg
        for i in range(padding_dx_n):
            temp += all_chars[random.randint(0, len(all_chars) - 1)]
        send_message_to_server_with_check(conn, ALPHABET_MSG, direct=True)
        for e in (padding_sx_n, padding_dx_n, byte_char, encription_level):
            fake_msg = ""
            for i in range(e):
                fake_msg += all_chars[random.randint(0, len(all_chars) - 1)]
            send_message_to_server_with_check(conn, fake_msg, direct=True)
        print(f"Encripted str: {last_encode(temp, encription_level)}")
        send_message_to_server_with_check(conn, last_encode(temp, encription_level))
        new_alphabet_decode = {}
        for n, char in enumerate(all_chars):
            new_alphabet_decode.update({new_alphabet_encode[char]: char})
        if not addr[0] in DECODE_ALPHABET:
            DECODE_ALPHABET.update({addr[0]: new_alphabet_decode})
        else:
            DECODE_ALPHABET[addr[0]] = new_alphabet_decode

        encode_args = byte_char, new_alphabet_encode, encription_level
        decode_args = byte_char, new_alphabet_decode, encription_level
        print(f"ENCODE_ALPHABET {addr[0]}:\n{ENCODE_ALPHABET}")
        print(f"DECODE_ALPHABET {addr[0]}:\n{DECODE_ALPHABET}")
        globals()[addr[0] + "_recv"] = None
        globals()[addr[0] + "_without_alph"] = False
        while connected:
            # try:
            msg = recv_with_long(conn, decode_args)
            print(f"MSG: {msg}")
            if msg == DISCONNECT_MESSAGE:
                disc = recv_with_long(conn, decode_args)
                if disc == "True":
                    if conn in clients_connected:
                        clients_connected.remove(conn)
                        for client in clients:
                            if client[0] == addr[0]:
                                clients.remove(client)
                                break
                connected = False
                #if disc != "True":
                #    print(f"Rimuovo alfabeto indirizzo: {addr[0]}\n{ENCODE_ALPHABET[addr[0]]}")
                #    del ENCODE_ALPHABET[addr[0]]
                #    del DECODE_ALPHABET[addr[0]]
            elif msg == RECV_MSG:
                globals()[addr[0]+"_recv"] = RECV_MSG
            elif msg == INFO_MSG_T1:
                print(str(clients).encode(FORMAT))
                send_message_to_server_with_check(conn, str(clients), encode_args)
            elif msg == INFO_MSG_T2:
                send_message_to_server_with_check(conn, INFO_MSG_T2, encode_args)
                for chat_room in chat_rooms:
                    if addr[0] in chat_room[2]:
                        current_client = []
                        for client in clients:
                            if client[0] in chat_room[2]:
                                current_client.append(client)
                        print(f"invio infomsg_t2: {addr[0]}")
                        send_message_to_server_with_check(conn, str(current_client), encode_args)
                        break

            elif msg == CHAT_ROOMS_MSG_T1:
                print(str(clients).encode(FORMAT))
                send_message_to_server_with_check(conn, str(chat_rooms), encode_args)
            elif msg == CHAT_ROOMS_MSG_T2:
                send_message_to_server_with_check(conn, CHAT_ROOMS_MSG_T2, encode_args)
                send_message_to_server_with_check(conn, str(chat_rooms), encode_args)
            elif msg == NAME_MSG:
                name = recv_with_long(conn, decode_args)
                clients.append([addr[0], name, None])
                print(f"Clients !NOME: {clients}")
                clients_connected.append(conn)
            elif msg == IP_MSG:
                send_message_to_server_with_check(conn, str(addr[0]), encode_args)
            elif msg == REPLACE_MSG:
                client_to_replace = ast.literal_eval(recv_with_long(conn, decode_args))
                for i, client in enumerate(clients):
                    if client[0] == client_to_replace[0]:
                        clients[i] = client_to_replace
                        break
            elif msg == CREATED_ROOM:
                print(clients_connected)
                adminip = recv_with_long(conn, decode_args)
                chat_rooms.append(
                    [[adminip], ast.literal_eval(recv_with_long(conn, decode_args)), [adminip],
                     [adminip]])
                print("Numero di clients: " + str(len(clients_connected)))
                print(clients)
                for client in clients:
                    if client[2] is None:
                        send_message_to_server_with_check(client[0], CREATED_ROOM, encode_args)
            elif msg == PASS_MSG:
                send_message_to_server_with_check(addr[0], PASS_MSG, encode_args)
            elif msg == RECONN_MSG:
                print("Clients collegati ", clients_connected)
                print("\n")
                for i, client_connected in enumerate(clients_connected):
                    print(
                        f"Client: {client_connected}, indice: {i}, indirizzo client: {client_connected.getpeername()[0]}, indirizzo di questo client: {addr}")
                    if client_connected.getpeername()[0] == addr[0]:
                        clients_connected[i] = conn
                        break

                print("Clients collegati ", clients_connected)
            elif msg == TO_JOIN_MSG:
                ips = ast.literal_eval(recv_with_long(conn, decode_args))
                print(f"Ips collegati: {ips}")
                this_client = []
                for client in clients:
                    if client[0] == addr[0]:
                        this_client = client
                        break
                print(f"Questo client: {this_client}")
                for i, chat_room in enumerate(chat_rooms):
                    if ips == chat_room[2]:
                        chat_rooms[i][2].append(this_client[0])
                        if this_client[0] not in chat_rooms[i][3]:
                            chat_rooms[i][3].append(this_client[0])
                        break
                print(f"Chat room:  {chat_rooms}")
                for client in clients:
                    if client[2] is None:
                        send_message_to_server_with_check(client[0], PASS_MSG, ENCODE_ALPHABET[client[0]])
                for ip in ips:
                    if ip != addr[0]:
                        for i, client_connected in enumerate(clients_connected):
                            print(f"Client collegati: {client_connected}")
                            if clients[i][0] == ip:
                                send_message_to_server_with_check(ip, JOINED, ENCODE_ALPHABET[ip])
                                send_message_to_server_with_check(ip, this_client[1], ENCODE_ALPHABET[ip])
                                print("TO_JOIN_MSG")
                                print("Clients --> ", clients)
                                break
            elif msg == NEW_CLIENT_MSG:
                send_message_to_server_with_check(conn, NEW_CLIENT_MSG, encode_args)
                send_message_to_server_with_check(conn, "Ti sei unito alla chat!", encode_args)
            elif msg == LEFT_CLIENT_MSG:
                this_client = []
                for client in clients:
                    if client[0] == addr[0]:
                        this_client = client
                for i, client in enumerate(clients):
                    if client[0] == this_client[0]:
                        clients[i] = this_client
                        break
                clients_to_chat = get_clients_to_chat(addr[0])
                for i, client_to_chat in enumerate(clients_to_chat):
                    send_message_to_server_with_check(client_to_chat, LEFT_CLIENT_MSG, encode_args)
                    send_message_to_server_with_check(client_to_chat, str(this_client), encode_args)
                for client in clients_connected:
                    for client_ in clients:
                        if client_[0] == client.getpeername()[0]:
                            if client_[2] is None:
                                send_message_to_server_with_check(client, PASS_MSG, encode_args)
                print("LEFT_CLIENT_MSG")
                print("Clients --> ", clients)
                this_client[2] = None
            elif msg == REMOVE_CLIENTS_TO_CHAT:
                exited_client = recv_with_long(conn, decode_args)
                print("client uscito ", exited_client)
                print(chat_rooms)
                for i, chat_room in enumerate(chat_rooms):
                    for client_ip in chat_room[2]:
                        if client_ip == addr[0]:
                            print("ip utente-> ", exited_client)
                            chat_rooms[i][2].remove(exited_client)
                            print("clientsss-> ", chat_rooms)
                            break
            elif msg == MESSAGE:  # aggiungine uno per i messaggi tipo !MESSAGE
                send_message_to_server_with_check(conn, RECV_MSG, encode_args)
                msg = recv_with_long(conn, decode_args, MESSAGE)
                this_client = []
                for client in clients:
                    if client[0] == addr[0]:
                        this_client = client
                clients_to_chat = get_clients_to_chat(addr[0])
                print(f"Clients ai quali viene mandato il messaggio {clients_to_chat}")
                for i, client_to_chat in enumerate(clients_to_chat):
                    send_message_to_server_with_check(client_to_chat, MESSAGE,
                                                      ENCODE_ALPHABET[client_to_chat.getpeername()[0]])
                    send_message_to_server_with_check(client_to_chat, this_client[1],
                                                      ENCODE_ALPHABET[client_to_chat.getpeername()[0]])
                    send_message_to_server_with_check(client_to_chat, msg,
                                                      ENCODE_ALPHABET[client_to_chat.getpeername()[0]])
                send_message_to_server_with_check(conn, RECV_MSG, encode_args)
            elif msg == ERROR_MSG:
                break
            time.sleep(0.05)
        # except Exception as e:
        #    print("Connessione in corso interrotta forzatamente dall'client remoto\n")
        #    print(e)
        #    connected = False
    print(f"\nIl thread associato all'indirizzo {addr[0]} è stato terminato!\n\n")


clients_connected = []
chat_rooms = []


def start():
    server.listen()
    print(f"[ASCOLTO] Il server è in ascolto all'indirizzo {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[CONNESSIONI ATTIVE] \n{threading.active_count() - 1}")


print("[AVVIO] Il server si sta avviando...")
start()
