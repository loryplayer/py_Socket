import getopt
import socket
import platform
import sys
import threading
import time
from subprocess import call
from commands import *
import Mousewheel_Support

OS = platform.system()


def create_client():
    root = Tk()
    root.title("Client")
    root.geometry("350x200")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    def on_closing():
        root.destroy()
        send_message_to_server_with_check(client, DISCONNECT_MESSAGE)
        send_message_to_server_with_check(client, "True")
        if OS == "Linux":
            call(['python3', 'Client_connection.py'])
        else:
            call('python Client_connection.py')
        sys.exit(1)

    def press_key(event):
        if event.keycode == 13:
            login()
        elif event.keycode == 27:
            on_closing()

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing())
    root.bind("<KeyPress>", press_key)
    refresh_remove_placeholder_bool()
    client_name = Entry(root, bd=2, relief="groove", font=('calibri', 16, 'bold'), fg="#8A8A8A", width=24,
                        justify='center')
    client_name.insert(END, "Inserisci il tuo nome")
    client_name.bind('<Button-1>', lambda event: remove_placeholder(event, client_name))
    client_name.bind('<FocusOut>', lambda event: leave(event, client_name, "Inserisci il tuo nome"))
    client_name.place(relx=0.5, rely=0.25, anchor=CENTER)
    client_name.bind("<KeyPress>", press_key)
    info_client = Label(root, font=('calibri', 12, 'bold'), fg="#8A8A8A",
                        text="Questo nome sarà visibile agli altri utenti\n che si collegheranno a questo server!")
    info_client.place(relx=0.5, rely=0.5, anchor=CENTER)
    error_label = Label(root, font=('calibri', 9, 'bold'), fg="#FF0000")
    error_label.place(relx=0.5, rely=0.1, anchor=CENTER)

    def login():
        if not client_name.get() == "Inserisci il tuo nome":
            if len(client_name.get()) <= MAX_CHAR_NAME:
                messages = [NAME_MSG, client_name.get()]
                for message in messages:
                    send_message_to_server_with_check(client, message)
                root.destroy()
                heandle_hub(None, ADDR)
            else:
                error_label["text"] = "Nome troppo lungo, supera i " + str(MAX_CHAR_NAME) + " caratteri!"
        else:
            error_label["text"] = "Devi compilare questo campo!"

    ok_btn = Button(root, font=('calibri', 16, 'bold'), fg="#646464", text="OK", command=login)
    ok_btn.place(relx=0.5, rely=0.75, anchor=CENTER, height=35)
    root.mainloop()


client = None
PORT = 0000
SERVER = ""


def create_hub(client_):
    global client
    client = client_
    create_client()


def sort(by):
    infos_sorted = []
    rooms_ = rooms[:]
    for room in rooms_:
        if by == "name":
            infos_sorted.append(room[1][1])
        elif by == "number":
            infos_sorted.append(str(len(room[2])))
    new_infos_sorted = []
    if by == "name":
        infos_sorted.sort()
        print(f"Info sorted: {infos_sorted}")
        numbers_str = []
        strs = []
        for i, info_sorted in enumerate(infos_sorted):
            number = ''
            found_number = False
            for info_sorted_char in info_sorted:
                if info_sorted_char.isnumeric():
                    number += info_sorted_char
                    found_number = True
                else:
                    break
            if not found_number:
                strs.append(info_sorted)
            else:
                numbers_str.append([int(number), info_sorted])

        for e in range(len(numbers_str)-1):
            if numbers_str[e][0] > numbers_str[e+1][0]:
                temp = numbers_str[e+1]
                numbers_str[e + 1] = numbers_str[e]
                numbers_str[e] = temp



        print(f"Numeri ordinati: {numbers_str}\nStringhe ordinate: {strs}")
        new_infos_sorted_str=[]
        [new_infos_sorted_str.append(number[1]) for number in numbers_str]
        new_infos_sorted_str.extend(strs)
        for names in new_infos_sorted_str:
            for i, info in enumerate(rooms_):
                if info[1][1] == names:
                    del (rooms_[i])
                    new_infos_sorted.append(info)
                    break


        '''
        for number in numbers:
            temp = 0
            for i, info_sorted in enumerate(infos_sorted):
                number_str = ''
                for info_sorted_char in info_sorted:
                    if info_sorted_char.isnumeric():
                        number_str += info_sorted_char
                    else:
                        break
                if str(number) == number_str:
                    new_infos_sorted_str.append(info_sorted)
                    temp = i
            del (infos_sorted[temp])
        for info_sorted in new_infos_sorted_str:
            for i, info in enumerate(rooms_):
                if info[1][1] == info_sorted:
                    del (rooms_[i])
                    new_infos_sorted.append(info)
                    break
        if strs:
            for string in rooms_:
                new_infos_sorted.append(string)
        '''
    elif by == "number":
        numbers = []
        for number in infos_sorted:
            numbers.append(int(number))
        numbers.sort()
        for number in numbers:
            for i, info in enumerate(rooms_):
                if len(info[2]) == number:
                    del (rooms_[i])
                    new_infos_sorted.append(info)
                    break
    return new_infos_sorted


def entry_on_chat_room(root, addr_ips):
    import Client
    global infos
    send_message_to_server_with_check(client, DISCONNECT_MESSAGE)
    send_message_to_server_with_check(client, "False")
    new_client = socket.socket()
    connect_to(new_client, ADDR)
    send_message_to_server_with_check(new_client, RECONN_MSG)
    this_client = get_current_client(new_client, get_infos(new_client))
    print("Questo client: " + str(this_client))
    this_client[2] = PART
    send_message_to_server_with_check(new_client, REPLACE_MSG)
    send_message_to_server_with_check(new_client, str(this_client))
    root.destroy()
    Client.client_manager(new_client, addr_ips, this_client, ADDR)


def show_clients(scrolling_area, rooms):
    global hub_root
    for widget in scrolling_area.innerframe.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    for i, client_on_server in enumerate(rooms):
        if client_on_server[1][0] == "public" or (
                client_on_server[1][0] == "private" and get_current_client(client, get_infos(client))[0] in
                client_on_server[3]):
            div = Frame(scrolling_area.innerframe, relief="solid", bd=2)
            div.pack(padx=2, pady=2, anchor="n", fill=X, expand=1)
            label = Label(div,
                          text=client_on_server[1][1],
                          font=('calibri', 16, 'bold'),
                          fg="#8A8A8A")
            label.pack(padx=15, anchor="w", side=LEFT)
            scrolling_area.update_viewport()
            label.update()
            width_name = (label.winfo_width())
            paddingx = 335 - width_name
            label = Label(div,
                          text=str(len(client_on_server[2])),
                          font=('calibri', 16, 'bold'),
                          fg="#8A8A8A")
            x = paddingx - len(str(len(client_on_server[2]))) * 4
            label.pack(padx=(x, 125), side=LEFT)
            enter_btn = Button(div,
                               text="Entra",
                               font=('calibri', 16, 'bold'),
                               fg="#8A8A8A")
            enter_btn["command"] = lambda: entry_on_chat_room(hub_root, client_on_server[2])
            enter_btn.place(height=50)
            enter_btn.update()
            enter_btn.pack(padx=(0, 20), pady=15, anchor="w", side=RIGHT)

    scrolling_area.update_viewport()


remove = False
order = ""


def change_state(scrolling_area, btns, btn_st, state, imgs):
    global remove, order
    orders = ["name", "number"]
    if state == 1:
        btns[btn_st]["image"] = imgs[1]
        btns[btn_st]["command"] = lambda new_state=0: change_state(scrolling_area, btns, btn_st, new_state, imgs)
        show_clients(scrolling_area, sort(orders[btn_st]))
    else:
        btns[btn_st]["image"] = imgs[0]
        btns[btn_st]["command"] = lambda new_state=1: change_state(scrolling_area, btns, btn_st, new_state, imgs)
        print(rooms)
        show_clients(scrolling_area, rooms)
    if btn_st == 1:
        order = "number"
        btns[0]["image"] = ""
        btns[0]["command"] = lambda new_state=1: change_state(scrolling_area, btns, 0, new_state, imgs)
    else:
        print("infos 4: ")
        order = "name"
        btns[1]["image"] = ""
        btns[1]["command"] = lambda new_state=1: change_state(scrolling_area, btns, 1, new_state, imgs)
    btns[btn_st].update()


infos = []
rooms = []
connected = True


def update():
    global infos, order, connected, rooms
    print("Io ora dovrei essere qui --> 2")
    while connected:
        print("Io ora dovrei essere qui --> 3")
       # while True:
       #     try:
        infos = get_infos(client)
       #         break
       #     except SyntaxError:
       #         pass
        this_profile = get_current_client(client, infos)
        rooms = get_rooms_t1(client)
        print("clientsss---------------")
        print(this_profile)
        print(rooms)
        print("fineclientsss---------------")
        if rooms:
            scrolling_area = Mousewheel_Support.Scrolling_Area(hub_root, relief="solid", bd=1)
            scrolling_area.place(x=1, width=598, height=351.5, rely=0.1)
            if order == "name" or order == "number":
                show_clients(scrolling_area, sort(order))
            else:
                show_clients(scrolling_area, rooms)
            arrow_imgs = ["img/uparrow.png", "img/downarrow.png"]
            texts = ["Nome della chat", "Utenti collegati"]
            imgs = []
            btns = []
            xs = [20, 320]
            for i in range(2):
                img_a = PhotoImage(file=arrow_imgs[i])
                img_b = img_a.subsample(1, 1)
                imgs.append(img_b)
                btn = Button(hub_root, text=texts[i], compound=TOP,
                             borderwidth=0, relief=SUNKEN, font=('calibri', 12, 'bold'),
                             fg="#646464")
                btn.place(x=xs[i], y=10)

                btns.append(btn)
            btns[0]["command"] = lambda: change_state(scrolling_area, btns, 0, 1, imgs)
            btns[0]["image"] = imgs[0]
            btns[1]["command"] = lambda: change_state(scrolling_area, btns, 1, 1, imgs)
        else:
            scrolling_area = Mousewheel_Support.Scrolling_Area(hub_root, relief="solid", bd=1)
            scrolling_area.place(x=1, width=598, height=351.5, rely=0.1)
            label = Label(scrolling_area.innerframe,
                          text="Non è presente nessuna stanza per chattare.\nCreane una con l'apposito bottone",
                          font=('calibri', 16, 'bold'),
                          fg="#8A8A8A")
            label.place(relx=0.5, rely=0.5, anchor=CENTER)

        def create_room_settings():
            hub_root.destroy()
            room_settings = Tk()
            room_settings.title("Impostazioni della chat")
            room_settings.geometry("350x250")
            room_settings.resizable(False, False)

            def on_closing():
                room_settings.destroy()
                send_message_to_server_with_check(client, PASS_MSG)
                heandle_hub(client, ADDR)

            def press_key(event):
                if event.keycode == 13:
                    create_room()
                elif event.keycode == 27:
                    on_closing()

            room_settings.bind("<KeyPress>", press_key)
            room_settings.protocol("WM_DELETE_WINDOW", on_closing)
            room_settings.attributes("-topmost", True)
            name_of_room_label = Label(room_settings, text="Nome della chat", font=('calibri', 16, 'bold'),
                                       fg="#8A8A8A")
            name_of_room_label.place(relx=0.5, rely=0.10, anchor=CENTER)
            name_of_room = Entry(room_settings, bd=2,
                                 relief="groove", font=('calibri', 12, 'bold'),
                                 fg="#8A8A8A", justify='center')
            name_of_room.insert(END, "Inserisci qui il nome della chat")
            name_of_room.place(relx=0.5, rely=0.25, anchor=CENTER, width=250, height=30)
            refresh_remove_placeholder_bool()
            name_of_room.bind('<Button-1>', lambda event: remove_placeholder(event, name_of_room))
            name_of_room.bind('<FocusOut>',
                              lambda event: leave(event, name_of_room, "Inserisci qui il nome della chat"))
            types_of_room_label = Label(room_settings, text="Scegli la modalità della stanza:",
                                        font=('calibri', 16, 'bold'),
                                        fg="#8A8A8A")
            types_of_room_label.place(relx=0.5, rely=0.40, anchor=CENTER, width=280, height=30)
            var = StringVar(room_settings, "public")
            types_of_room = {"Privata": "private", "Pubblica": "public"}
            for e, (text, value) in enumerate(types_of_room.items()):
                Radiobutton(room_settings, text=text, variable=var, value=value, font=('calibri', 12, 'bold'),
                            fg="#8A8A8A").place(relx=0.35, rely=0.55 - (e / 10))

            def create_room():
                global connected
                import Client
                connected = False
                this_profile[2] = PART
                messages = [REPLACE_MSG, str(this_profile), CREATED_ROOM, this_profile[0],
                            str([var.get(), name_of_room.get()])]
                for message_ in messages:
                    send_message_to_server_with_check(client, message_)
                room_settings.destroy()
                send_message_to_server_with_check(client, DISCONNECT_MESSAGE)
                send_message_to_server_with_check(client, "False")
                new_client = socket.socket()
                connect_to(new_client, ADDR)
                send_message_to_server_with_check(new_client, RECONN_MSG)
                Client.client_manager(new_client, "all", this_profile, ADDR)

            create_room_btn = Button(room_settings, text="Crea!", font=('calibri', 12, 'bold'),
                                     fg="#646464", command=create_room)
            create_room_btn.place(relx=0.40, rely=0.7, width=80)
            room_settings.mainloop()

        add_client_rooms = Button(hub_root, text="Crea una chat", font=('calibri', 16, 'bold'),
                                  fg="#646464", command=create_room_settings)
        add_client_rooms.place(relx=0.5, rely=0.9, anchor=CENTER)
        recv_with_long(client)
        print("test")
        try:
            scrolling_area.destroy()
        except RuntimeError:
            break
        for widget in hub_root.winfo_children():
            print(type(widget))
            if isinstance(widget, Button):
                widget.destroy()
        # scrolling_area.update_viewport(y="Center")


ADDR = ()


def heandle_hub(client_, ADDR_):
    global hub_root, client, connected, ADDR
    ADDR = ADDR_
    if client_ is not None:
        print("Forse dovrei essere anche qua!")
        client = client_
    hub_root = Tk()
    hub_root.title("Client")
    hub_root.geometry("600x500")
    hub_root.resizable(True, True)
    hub_root.attributes("-topmost", True)
    connected = True

    def press_key(event):
        if event.keycode == 27:
            on_closing()

    def on_closing():
        hub_root.destroy()
        send_message_to_server_with_check(client, DISCONNECT_MESSAGE)
        send_message_to_server_with_check(client, "True")
        if OS == "Linux":
            call(['python3', 'Client_connection.py'])
        else:
            call('python Client_connection.py')

    hub_root.bind("<KeyPress>", press_key)
    hub_root.protocol("WM_DELETE_WINDOW", on_closing)
    thread = threading.Thread(target=update, args=())
    thread.daemon = True
    thread.start()
    hub_root.mainloop()


if __name__ == "__main__":
    try:
        full_cmd_arguments = sys.argv
        argument_list = full_cmd_arguments[1:]
    except getopt.error as err:
        sys.exit(2)

    SERVER = argument_list[0].replace("--", "")
    PORT = argument_list[1].replace("\n", "")
    ADDR = (SERVER, int(PORT))

    client = socket.socket()
    connect_to(client, ADDR)

    create_hub(client)
