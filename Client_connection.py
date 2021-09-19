import socket
from commands import *
from tkinter import *
from subprocess import call
import sys
import platform

auto_access = False
auto_access_as_admin = False
auto_create_chat = False
if auto_access:
    SERVER="25.70.218.163"
    PORT = 5050
    address = ("25.70.218.163", 5050)
    client = socket.socket()
    client.connect(address)
    messages = [NAME_MSG, "ADMIN" if auto_access_as_admin else "Test"]
    for message in messages:
        send_message_to_server_with_check(client, message)
    if auto_create_chat:
        infos = get_infos(client)
        this_profile = get_current_client(client, infos)
        this_profile[2] = PART
        messages = [REPLACE_MSG, str(this_profile), CREATED_ROOM, this_profile[0],
                    str(["private" if auto_access_as_admin else "public", "TEST"])]
        for message_ in messages:
            send_message_to_server_with_check(client, message_)
        import Client
        send_message_to_server_with_check(client, DISCONNECT_MESSAGE)
        send_message_to_server_with_check(client, "False")
        new_client = socket.socket()
        new_client.connect(address)
        send_message_to_server_with_check(new_client, RECONN_MSG)
        Client.client_manager(new_client, "all", this_profile, address)
    else:
        import Client_hub
        Client_hub.heandle_hub(client, (SERVER, int(PORT)))
else:
    root = Tk()
    root.geometry("520x250")
    root.title("Client Connection")
    root.resizable(False, False)
    root.attributes("-topmost", True)


    def on_closing():
        print("Uscita 1")
        sys.exit(1)


    root.protocol("WM_DELETE_WINDOW", on_closing)
    main_frame = Frame(root, bd=1, relief="solid")

    div_label = Label(main_frame, text="Collegati a un server esistente", font=('calibri', 16, 'bold'))
    div_label.place(rely=0.15, relx=0.25)

    server_text = Entry(main_frame, bd=2, relief="groove", font=('calibri', 16, 'bold'), fg="#8A8A8A", width=24,
                        justify='center')
    server_text.pack(side=LEFT, pady=50, padx=2)
    server_text.insert(END, "Indirizzo del server")

    div_label = Label(main_frame, text=":", width=1, font=('calibri', 16, 'bold'))
    div_label.pack(side=LEFT)

    port_text = Entry(main_frame, bd=2, relief="groove", font=('calibri', 16, 'bold'), fg="#8A8A8A", justify='center')
    port_text.pack(side=LEFT, pady=50, padx=2)
    port_text.insert(END, "Porta del server")
    remove_placeholder_bool = [True, True]


    def access():
        try:
            server = (server_text.get())
            port = int(port_text.get())
            address = (server, port)
            client = socket.socket()
            client.settimeout(0.5)
            client.connect(address)
            send_to_server(client, TEST_MSG.encode(FORMAT))
            msg_rec = recv(client).decode(FORMAT)
            print(msg_rec)
            if msg_rec == "False":
                client.close()
                root.destroy()
                OS = platform.system()
                if OS == "Linux":
                    call(['python3', 'Client_hub.py', server, str(port)])
                else:
                    call('python Client_hub.py --' + server + ' ' + str(
                        port))
            else:
                error = Label(main_frame, font=('calibri', 16, 'bold'), fg="#8A8A8A",
                              text="Ti sei già collegato a questo server!")
                error.place(relx=0.23, rely=0.85, height=30)
        except socket.timeout:
            error = Label(main_frame, font=('calibri', 16, 'bold'), fg="#8A8A8A",
                          text="Il server inserito non è raggiungibile")
            error.place(relx=0.23, rely=0.85, height=30)
        except socket.gaierror:
            error = Label(main_frame, font=('calibri', 16, 'bold'), fg="#8A8A8A",
                          text="Il server inserito è errato")
            error.place(relx=0.32, rely=0.85, height=30)


    ok_button = Button(main_frame, font=('calibri', 16, 'bold'), fg="#646464", text="Accedi", command=access)
    ok_button.place(relx=0.45, rely=0.65, height=30)


    def remove_placeholder(event, num):
        global remove_placeholder_bool
        if remove_placeholder_bool[num]:
            if num == 0:
                remove_placeholder_bool[num] = False
                server_text.delete(0, "end")
            elif num == 1:
                remove_placeholder_bool[num] = False
                port_text.delete(0, "end")
        else:
            if num == 0:
                pass
            elif num == 1:
                pass


    def leave(event, num):
        if num == 0:
            if server_text.get() == "" or server_text.get() == " ":
                server_text.delete(0, "end")
                server_text.insert(END, "Indirizzo del server")
                remove_placeholder_bool[num] = True
                server_text.update()
        elif num == 1:
            if port_text.get() == "" or port_text.get() == " ":
                port_text.delete(0, "end")
                port_text.insert(END, "Porta del server")
                remove_placeholder_bool[num] = True
                port_text.update()


    def press_key(event):
        if event.keycode == 13:
            access()
        elif event.keycode == 27:
            on_closing()


    server_text.bind('<Button-1>', lambda event: remove_placeholder(event, 0))
    port_text.bind('<Button-1>', lambda event: remove_placeholder(event, 1))
    server_text.bind('<FocusOut>', lambda event: leave(event, 0))
    port_text.bind('<FocusOut>', lambda event: leave(event, 1))
    server_text.bind("<KeyPress>", press_key)
    port_text.bind("<KeyPress>", press_key)
    root.bind("<KeyPress>", press_key)
    main_frame.place(height=250)
    root.mainloop()
