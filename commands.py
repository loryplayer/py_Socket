import ast
import base64
import codecs
from tkinter import *

FORMAT = 'utf-8'
PART = "participate"
DISCONNECT_MESSAGE = "!DISCONNESSO"
TEST_MSG = "!TEST"
INFO_MSG_T1 = "!INFO_T1"
INFO_MSG_T2 = "!INFO_T2"
CHAT_ROOMS_MSG_T1 = "!CHAT_ROOMS_T1"
CHAT_ROOMS_MSG_T2 = "!CHAT_ROOMS_T2"
NAME_MSG = "!NOME"
REPLACE_MSG = "!RIMPIAZZA"
CREATED_ROOM = "!STANZACREATA"
PASS_MSG = "!PASS"
TO_JOIN_MSG = "!PERUNIRSI"
NEW_CLIENT_MSG = "!NUOVOCLIENT"
JOINED = "!UNITO"
LEFT_CLIENT_MSG = "!USCITO"
MESSAGE = "!MESSAGGIO"
ALPHABET_STR_MSG = "!ALFABETO"
NORMAL_MESSAGE = "!N_MSG"
LONG_MESSAGE = "!L_MSG"
END_LONG_MESSAGE = "!F_L_MSG"
RECONN_MSG = "!RICONNETTI"
RECV_MSG = "!RICEVUTO"
REMOVE_CLIENTS_TO_CHAT = "!RIMUOVI"
HEADER = 3
ALPHABET_STR = ""
LIMIT_SHOW_MSG = 60
LIMIT_SHOW_MSG -= 1
MAX_CHAR_NAME = 20
DECODE_ALPHABET = {}
ENCODE_ALPHABET = {}
scrolling_y = 1
byte_char = 2
all_byes = 256
encription_level = 0
all_chars = ""
for i in range(all_byes):
    all_chars += (chr(i))


def send_to_server(client, msg, encoded=False):
    message = msg
    msg_lenght = len(message)
    send_length = str(msg_lenght).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    print(f"\n\nMessaggio da inviare </{msg}/>\nLunghezza del messaggio da inviare {send_length}")
    client.send(send_length)
    client.send(message)


def get_infos(client):
    send_message_to_server_with_check(client, INFO_MSG_T1)
    rec_msg = recv_with_long(client, True)
    return ast.literal_eval(rec_msg)


def get_rooms_t1(client):
    send_message_to_server_with_check(client, CHAT_ROOMS_MSG_T1)
    rec_msg = recv_with_long(client, True)
    return ast.literal_eval(rec_msg)


def get_current_client(client, clients):
    this_profile = []
    client_ip = client.getpeername()[0]
    print(f"Indirizzo ip corrente {client_ip}")
    for i, client_on_server in enumerate(clients):
        print(f"Confronto {client_on_server[0]}")
        if client_on_server[0] == client_ip:
            this_profile = client_on_server
    return this_profile


def recv(client, decode=False):
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length.strip())
        msg = client.recv(msg_length)
        print(f"\n\nLunghezza del messaggio da ricevere {msg_length}\nMessaggio da ricevere </{msg}/>")
        print("\nDimensione del messaggio ricevuto:")
        print(f"Corretta") if msg_length == len(msg) else print(
            f"Errata\nDimensione del messaggio da ricevere: {msg_length}\nDimensione del messaggio effettivo: {len(msg)}")
        return msg if not decode else msg.decode(FORMAT)
    else:
        print(f"\n\nErrore di ricezione da:   {client.getpeername()}\nMessaggio da ricevere {msg_length}")


def get_key(alf, val):
    for key, value in alf.items():
        if val == value:
            return key

    return "key doesn't exist"


def decode(byte):
    try:
        return byte.decode(FORMAT)
    except UnicodeError:
        str = first_decode(byte, encription_level)
        re = ""
        print(DECODE_ALPHABET)
        for n in range(int(len(str) / byte_char)):
            re += DECODE_ALPHABET[str[byte_char * n:byte_char * n + byte_char]]
        return re


def encode(string, alphabet_=False):
    if alphabet_ is False:
        if isinstance(string, str):
            return string.encode(FORMAT)
        else:
            return string
    string_encoded = ""
    for char in string:
        string_encoded += alphabet_[char]
    return last_encode(string_encoded)


def last_encode(alf):
    r = ""
    for i in range(encription_level):
        r = str(str(alf).encode(FORMAT))
        r = r[2:len(r) - 1].encode("ascii")
        r = base64.b64encode(r)
    r = str(r)
    r = r[2:len(r) - 1]
    r = r.encode("utf-16")
    return r


def recv_with_long(conn, decode_=False):
    message_type_long = recv(conn, decode=True)
    msg = b""
    print(f"TIPO MESSAGGIO: {message_type_long}")
    if message_type_long == NORMAL_MESSAGE:
        msg = recv(conn)
    elif message_type_long == LONG_MESSAGE:
        msg += recv(conn)
        while True:
            send_message_to_server_with_check(conn, RECV_MSG, alphabet_=False)
            message_type_long = recv(conn, decode=True)
            if message_type_long == END_LONG_MESSAGE:
                break
            msg += recv(conn)
    decoded_msg = decode(msg) if decode_ else msg
    print(f"Msg decoded recv: {decoded_msg}")
    # print(f"\n\nLunghezza del messaggio da ricevere {len(decoded_msg)}\nMessaggio da ricevere </{decoded_msg}/>")
    # print("\nDimensione del messaggio ricevuto:")
    return decoded_msg


remove_placeholder_bool = [True, True]

recv_bool_block = False
send_message_counter = 0
messages_to_send = []


def send_message_to_server_with_check(client, msg, direct=True, alphabet_=None):
    if alphabet_ is None:
        alphabet_ = ENCODE_ALPHABET
        print(f"Alf:: {ENCODE_ALPHABET}")
        print(f"Alf:: {DECODE_ALPHABET}")
    print("INIZIO INVIO")
    print(f"MESSAGGIO NON CODIFICATO: {msg}")
    msg = encode(msg, alphabet_)
    if len(str(len(msg))) <= HEADER:
        print("MESSAGGIO CORTO")
        store_message(client, encode(NORMAL_MESSAGE), msg, direct)
    else:
        piece_msg = "9"
        header_str = ""
        for i in range(HEADER):
            header_str += "9"
            piece_msg += "9"
        while len(piece_msg) > HEADER:
            piece_msg = msg[:int(header_str)]
            msg = msg[int(header_str):]
            if len(piece_msg) != 0:
                store_message(client, encode(LONG_MESSAGE), piece_msg, direct)
        store_message(client, encode(END_LONG_MESSAGE), None, direct)


def store_message(client, message_type_long, msg, direct):
    global recv_bool_block
    print(f"recv_bool: {recv_bool_block}")
    if not recv_bool_block or direct:
        print("INVIO MESSAGGIO")
        if not direct:
            recv_bool_block = True
        send_to_server(client, message_type_long)
        if not message_type_long == END_LONG_MESSAGE.encode(FORMAT):
            send_to_server(client, msg)
    else:
        print("SALVATAGGIO MESSAGGIO")
        messages_to_send.append([client, message_type_long, msg])
    print(messages_to_send)


def send_message_to_server():
    global messages_to_send, recv_bool_block
    if messages_to_send:
        send_to_server(messages_to_send[0][0], messages_to_send[0][1])
        if not messages_to_send[0][1] == END_LONG_MESSAGE.encode(FORMAT):
            send_to_server(messages_to_send[0][0], messages_to_send[0][2])
        messages_to_send.remove(messages_to_send[0])
    else:
        recv_bool_block = False


def first_decode(bytes, encription_level):
    print(f"bytes qui: {bytes}")
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


def connect_to(client, addr):
    global byte_char, encription_level, ALPHABET_STR, DECODE_ALPHABET, ENCODE_ALPHABET
    client.connect(addr)
    send_message_to_server_with_check(client, PASS_MSG, alphabet_=False)
    alf_msg = recv_with_long(client).decode(FORMAT)
    if alf_msg == ALPHABET_STR_MSG:
        padding_sx_n = len(recv_with_long(client, False).decode(FORMAT))
        print(f"padding_sx_n: {padding_sx_n}")
        padding_dx_n = len(recv_with_long(client, False).decode(FORMAT))
        print(f"padding_dx_n: {padding_dx_n}")
        byte_char = len(recv_with_long(client, False).decode(FORMAT))
        print(f"byte_char: {byte_char}")
        encription_level = len(recv_with_long(client, False).decode(FORMAT))
        print(f"encription_level: {encription_level}")
        alphabet_str_temp = recv_with_long(client, False)
        print(f"alphabet_str_temp: {alphabet_str_temp}")
        alphabet_str_temp = first_decode(alphabet_str_temp, int(encription_level))
        print(f"alphabet_str_temp_1: {alphabet_str_temp}")
        ALPHABET_STR = alphabet_str_temp[padding_sx_n:len(alphabet_str_temp) - padding_dx_n]
        print(f"Byte per carattere: {byte_char}")
        print(f"Alfabetooo: {ALPHABET_STR}")
        DECODE_ALPHABET = {}
        for n, char in enumerate(all_chars):
            DECODE_ALPHABET.update({ALPHABET_STR[byte_char * n:byte_char * n + byte_char]: char})
        ENCODE_ALPHABET = {}
        for n, char in enumerate(all_chars):
            ENCODE_ALPHABET.update({char: get_key(DECODE_ALPHABET, char)})
        print(f"DECODE_ALPHABET: {DECODE_ALPHABET}")
        print(f"ENCODE_ALPHABET: {ENCODE_ALPHABET}")


def refresh_remove_placeholder_bool():
    global remove_placeholder_bool
    remove_placeholder_bool = True


def get_remove_placeholder_bool():
    global remove_placeholder_bool
    return remove_placeholder_bool


def set_remove_placeholder_bool(bool):
    global remove_placeholder_bool
    remove_placeholder_bool = bool


def remove_placeholder(event, entry):
    global remove_placeholder_bool
    if remove_placeholder_bool:
        remove_placeholder_bool = False
        entry.delete(0, "end")


def leave(event, entry, string):
    global remove_placeholder_bool
    if entry.get() == "" or entry.get() == " ":
        entry.delete(0, "end")
        entry.insert(END, string)
        remove_placeholder_bool = True
        entry.update()


def scroll_event(event, canvas, y=None):
    all_elemets_on_this_canvas = canvas.find_all()
    print(event)
    print(
        f"MSGS: {len(all_elemets_on_this_canvas)}\nPRIMO ITEM: {canvas.bbox(all_elemets_on_this_canvas[len(all_elemets_on_this_canvas) - 1])}")
    # print(f"\nLast msg: {canvas.itemcget(all_elemets_on_this_canvas[len(all_elemets_on_this_canvas) - 1], 'text')}\n")
    if canvas.bbox(all_elemets_on_this_canvas[len(all_elemets_on_this_canvas) - 1])[3] > 590 or \
            canvas.bbox(all_elemets_on_this_canvas[0])[3] < 0:
        if y is None:
            canvas.yview_scroll(-scrolling_y * int(event.delta / 120), "units")
        else:
            canvas.yview_scroll(scrolling_y if y < 0 else -scrolling_y, "units")
    canvas.update()


def bbox(element):
    x = element.winfo_x()
    y = element.winfo_y()
    width = element.winfo_width()
    height = element.winfo_height()
    x_btn_1 = x
    y_btn_1 = y
    x_btn_2 = x + width
    y_btn_2 = y + height
    return x_btn_1, y_btn_1, x_btn_2, y_btn_2


distance_msg_y_position = 25
distance_msg_y_position_last_msg = 20
start_padding = 50
distance_msg_y_position_time = 25


def place_object(scrolling_area, command, coords, **kwargs):
    item_id = command(coords, **kwargs)
    this_msg_bbox = scrolling_area.bbox(item_id)
    # print(f"\n\nCOORDINATE OGGETTO: {scrolling_area.coords(item_id)}")
    # print(f"COORDINATE VERTICI: {this_msg_bbox}")
    msg_show_x1 = this_msg_bbox[0]
    msg_show_y1 = this_msg_bbox[1]
    msg_show_x2 = this_msg_bbox[2]
    msg_show_y2 = this_msg_bbox[3]
    msg_show_width = abs(msg_show_x2 - msg_show_x1)
    msg_show_height = abs(msg_show_y2 - msg_show_y1)
    new_x = msg_show_width / 2
    new_y = msg_show_height / 2
    scrolling_area.move(item_id, new_x, new_y)
    # print("DOPO:")
    # print(f"\n\nCOORDINATE OGGETTO: {scrolling_area.coords(item_id)}")
    # print(f"COORDINATE VERTICI: {scrolling_area.bbox(item_id)}\n\n")
    return item_id
