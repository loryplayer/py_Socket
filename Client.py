#    ~  Copyright (c) 2021. Lorenzo Londero

import random
import socket
import platform
from tkinter.colorchooser import askcolor

from commands import *
import tkinter.scrolledtext as scrolledtext

try:
    import pyperclip
except ModuleNotFoundError:
    import getpass

    username = getpass.getuser()
    print(username)
    import os
    import subprocess
    import sys

    py_folder = f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\pyperclip"
    from distutils.dir_util import copy_tree
    import pathlib

    this_path = str(pathlib.Path(__file__).parent.resolve()) + "\\Libs\\pyperclip"
    print(this_path)
    import os, shutil

    os.mkdir(py_folder)


    def copytree(src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            print(f"S: {s}")
            d = os.path.join(dst, item)
            print(f"S: {d}")
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)


    copytree(this_path, py_folder)
    import pyperclip
from functools import partial
import datetime
import ast
import time
import threading

"""
count_of_animation = 0
number_of_btns = 0
pos = 800
posorigin = pos
posbackup = 0
postrans = 14
animation = True
"""
repress_animation_bools = [[[]]]
btn_objects = []
distances = [[]]
backup_position = 0


def set_animenation_variables(root, objects, type_of_objects, number_of_animation, pos, time_of_single_animation,
                              position_repress=None, btn_object=None, place_of_animation="on_gui",
                              chat_scrolling_area=None):
    def anim_handle():
        for i, repress_animation_bool in enumerate(repress_animation_bools):
            if btn_object == repress_animation_bool[0]:
                repress_animation_bools[i][3] = True
                e = i

        print(f"\n--------------------\n{repress_animation_bools}\n--------------------\n")

        def do_option_animation(obj, new_pos, distances, e_):
            root.update() if place_of_animation != "on_show_msg_box" else chat_scrolling_area.update()
            btn_ax = obj.winfo_x() if place_of_animation != "on_show_msg_box" else chat_scrolling_area.coords(obj)[0]
            btn_ay = obj.winfo_y() if place_of_animation != "on_show_msg_box" else chat_scrolling_area.coords(obj)[1]
            btn_bx = new_pos[0] + distances[counter_dis][1][e_][0]
            btn_by = new_pos[1] + distances[counter_dis][1][e_][1]

            print(f"Oggetto numero: {e_}")
            btn_bx_transition = abs(btn_bx - btn_ax) / number_of_animation
            btn_by_transition = abs(btn_by - btn_ay) / number_of_animation
            print(
                f"\n\n------\n{obj}--\nBTN_AX: {btn_ax}\nBTN_AY: {btn_ay}\nBTN_BX: {btn_bx}\nBTN_BY: {btn_by}\nBTN_BX_TRANSITION: {btn_bx_transition}\nBTN_BY_TRANSITION: {btn_by_transition}\n------\n\n")
            print(f"{repress_animation_bools}\n")
            if btn_bx < btn_ax:
                btn_bx_transition *= -1
            if btn_by < btn_ay:
                btn_by_transition *= -1
            for i_ in range(number_of_animation + 1):
                # print(
                #     f"Animazione 1:\nBTN posxa: {btn_ax}, BTN posya: {btn_ay}\nBTN posxb: {btn_bx}, BTN posyb: {btn_by}\n"
                #     f"Posizione reale x: {btn_ax + btn_bx_transition * i_}\nPosizione reale y: {btn_ay + btn_by_transition * i_}\n"
                #     f"Transizione asse x: {btn_bx_transition}\n"
                #     f"Transizione asse y: {btn_by_transition}\n")
                if repress_animation_bools[e][1]:
                    print(f"Repress_animation: {repress_animation_bools}\n")
                    break
                if place_of_animation == "on_gui":
                    obj.place_configure(x=btn_ax + btn_bx_transition * i_)
                    obj.place_configure(y=btn_ay + btn_by_transition * i_)
                elif place_of_animation == "on_show_msg_box":
                    chat_scrolling_area.move(obj, btn_bx_transition, btn_by_transition)
                if repress_animation_bools[e][1]:
                    print(f"Repress_animation: {repress_animation_bools}\n")
                    break
                root.update()
                time.sleep(time_of_single_animation)  # time.sleep(0.005)
            print(
                f"\nPOSIZIONE FINALE OBJ: ({obj.winfo_x() if place_of_animation != 'on_show_msg_box' else chat_scrolling_area.coords(obj)[0]},{obj.winfo_y() if place_of_animation != 'on_show_msg_box' else chat_scrolling_area.coords(obj)[1]})\n")
            if place_of_animation == "on_show_msg_box":
                chat_scrolling_area.move(obj, -chat_scrolling_area.coords(obj)[0], -chat_scrolling_area.coords(obj)[1])
                print(f"POSITIONNNNNN: {chat_scrolling_area.coords(obj)}")
                chat_scrolling_area.move(obj, btn_bx, btn_by)

        counter_dis = 0
        for h in distances:
            if objects not in h:
                counter_dis += 1
            else:
                break
        print(f"Counter: {counter_dis}")
        if counter_dis == len(distances):
            print("presente")
            distances.append([objects, [[0, 0]]])
            for i in range(len(objects) - 1):
                distances[counter_dis][1].append([
                    abs(objects[i].winfo_x() - objects[i + 1].winfo_x())
                    if objects[i].winfo_x() < objects[i + 1].winfo_x()
                    else -abs(objects[i].winfo_x() - objects[i + 1].winfo_x()),
                    abs(objects[i].winfo_y() - objects[i + 1].winfo_y())
                    if objects[i].winfo_y() < objects[i + 1].winfo_y()
                    else -abs(objects[i].winfo_y() - objects[i + 1].winfo_y())])
                print(f"DIST --> {distances}\ni: {i}\nCounter: {counter_dis}")
                distances[counter_dis][1][i + 1][0] += distances[counter_dis][1][i][0]
                distances[counter_dis][1][i + 1][1] += distances[counter_dis][1][i][1]
            # da completare facendo le somme delle distanze precedenti

        print(f"\n-----------------------\nDistanze:{distances}\n-----------------------\n")

        if not repress_animation_bools[e][2]:
            positions = position_repress
        else:
            positions = pos

        def calcolo_posizioni(object_, i_, offset_x_, offset_y_):
            root.update()
            print(f"\n\nPOSIZIONI: {positions}\n\n, POSREAL: {pos}")
            for _, position in enumerate(positions):
                print(f"---------------------------\nOggetto numero: {i_}\n"
                      f"Poszione numero: {_}"
                      f"Posizione corrente per l'oggetto {object_} senza offset: {position}\n"
                      f"Posizione corrente per l'oggetto {object_} con offset: {position[0] + offset_x_, position[1] + offset_y_}\nOffset x: {offset_x_}\nOffset y: {offset_y_}\n")
                if repress_animation_bools[e][1]:
                    print(f"Repress_animation: {repress_animation_bools}\n")
                    break
                do_option_animation(object_, position, distances, i_)
                if repress_animation_bools[e][1]:
                    print(f"Repress_animation: {repress_animation_bools}\n")
                    break
                root.update()
            print(f"---------------------------\n"
                  f"{repress_animation_bools}\n")

        offset_x = 0
        offset_y = 0
        for i, object in enumerate(objects):
            object.update() if place_of_animation == "on_gui" else None
            print(
                f"\nTesto sull'oggetto:{object['text'] if place_of_animation == 'on_gui' else chat_scrolling_area.itemcget(object, 'text')}\n")
            if repress_animation_bools[e][1]:
                print(f"Repress_animation: {repress_animation_bools}\n")
                break
            calcolo_posizioni(object, i, offset_x, offset_y)
            if repress_animation_bools[e][1]:
                print(f"Repress_animation : {repress_animation_bools}\n")
                break

        if repress_animation_bools[e][3]:
            repress_animation_bools[e][3] = False
        if repress_animation_bools[e][1]:
            repress_animation_bools[e][1] = False
            print("RIAVVIOOOOOOO")
            repress_animation_bools[e][2] = not repress_animation_bools[e][2]
            anim_handle()
            return

        print(
            f"\nFine animazione\n--------------------\n{btn_object} - {repress_animation_bools}\n--------------------\n")

    def stop_animation(cont):
        # def wait():
        #    while True:
        #        print(repress_animation_bools[cont])
        #        if not repress_animation_bools[cont][3]:
        #            print("\nANIMAZIONE INIZIATA RIPRESSIONE\n/")
        #            repress_animation_bools[cont][2] = not repress_animation_bools[cont][2]
        #            repress_animation_bools[cont][1] = False
        #            print(f"{repress_animation_bools}")
        #            break
        #        time.sleep(0.5)
        # Il click mentre l'animazione di ritorno è in funzione non va
        if repress_animation_bools[cont][3]:
            if not repress_animation_bools[cont][1]:
                repress_animation_bools[cont][1] = True
        else:
            repress_animation_bools[cont][2] = not repress_animation_bools[cont][2]
            anim_handle()
        # thread = threading.Thread(target=wait)
        # thread.daemon = True
        # thread.start()

    counter = 0
    found = False
    for counter, repress_animation_bool in enumerate(repress_animation_bools):
        if btn_object == repress_animation_bool[0]:
            found = True
            break
    print(counter, len(repress_animation_bools), found)
    if not found:
        repress_animation_bools.append([btn_object, False, True, True])
        anim_handle()
    elif type_of_objects == "options":
        stop_animation(counter)
    elif type_of_objects == "showed_msgs":
        if not repress_animation_bools[counter][3]:
            anim_handle()


scrolling_y = 1
distance_msg_y_position = 25
distance_msg_y_position_last_msg = 20
start_padding = 100
distance_msg_y_position_time = 25


def client_manager(client, addr_ips, this_profile, ADDR):
    last_name_client = ""
    all_showed_names_msgs = []
    all_showed_msgs_ids = []
    btns_config = []
    btns_sub_configs = []
    configurations = [["Gestisci chat", "Membri", "Segnala", "Abbandona"], "Informazioni"]
    this_room = []
    print(f"SERVER {ADDR[0]}, PORT {int(ADDR[1])}")
    if addr_ips != "all":
        send_message_to_server_with_check(client, TO_JOIN_MSG)
        send_message_to_server_with_check(client, str(addr_ips))
        send_message_to_server_with_check(client, NEW_CLIENT_MSG)
        globals()["CHAT_CREATED_bool"] = False
    else:
        globals()["RECV_bool"] = True
        globals()["CHAT_CREATED_bool"] = True
        globals()["CHAT_CREATED_str"] = "Hai creato la chat!"
    print("Il tuo client: ", this_profile)
    if this_profile[2] is not None:
        _layers = []

        def gui():
            def raise_frame(frame):
                frame.tkraise()

            root = Tk()
            root.title("Client")
            root.geometry("800x700")
            # root.resizable(False, False)
            root.attributes("-topmost", True)
            chat_frame = Frame(root)
            chat_frame.place(x=0, y=0, width=800, height=700)
            members_frame = Frame(root)
            members_frame.place(x=0, y=0, width=800, height=700)
            raise_frame(chat_frame)
            bottom_nav = Label(chat_frame, relief="solid", bd=1)
            chat_scrolling_area = Canvas(chat_frame, bd=1, relief="solid")
            chat_scrolling_area.config(scrollregion=chat_scrolling_area.bbox("all"))
            chat_scrolling_area.place(x=1, width=798, height=591.5)
            globals()["chat_scrolling_area"] = chat_scrolling_area
            chat_scr = Scrollbar(chat_scrolling_area)
            chat_scrolling_area.config(yscrollcommand=chat_scr.set)
            chat_scr.config(command=chat_scrolling_area.yview)

            def add_to_layer(command, coords, **kwargs):
                item_id = command(coords, **kwargs)
                return item_id

            OS = platform.system()
            if OS == "Linux":
                chat_scrolling_area.bind("<Button-4>", lambda event: scroll_event(event, chat_scrolling_area, 1))
                chat_scrolling_area.bind("<Button-5>", lambda event: scroll_event(event, chat_scrolling_area, -1))
            else:
                chat_scrolling_area.bind("<MouseWheel>", lambda event: scroll_event(event, chat_scrolling_area))

            def copy_msg(event, msg_showed, time_showed=None):
                print(chat_scrolling_area.itemcget(msg_showed, "text"))
                set_animenation_variables(chat_frame, [msg_showed],
                                          "showed_msgs", 5,
                                          [[chat_scrolling_area.coords(msg_showed)[0] + 5,
                                            chat_scrolling_area.coords(msg_showed)[1]],
                                           [chat_scrolling_area.coords(msg_showed)[0] - 5,
                                            chat_scrolling_area.coords(msg_showed)[1]],
                                           [chat_scrolling_area.coords(msg_showed)[0],
                                            chat_scrolling_area.coords(msg_showed)[1]]],
                                          btn_object=msg_showed,
                                          time_of_single_animation=0.002,
                                          place_of_animation="on_show_msg_box",
                                          chat_scrolling_area=chat_scrolling_area)
                pyperclip.copy(chat_scrolling_area.itemcget(msg_showed, "text"))

            def show_msg(msg, fg, font=('calibri', 14, 'bold'), bd=1, relief="solid", orientation=RIGHT, show_time=True,
                         name=None, color_name="#123456", padding=True, pady=10):
                global distance_msg_y_position_last_msg, gui
                if not "" == msg:
                    msg_phrase = msg.split("\n")
                    if len(msg) > LIMIT_SHOW_MSG:
                        msg_lines = []
                        counter = 0
                        for phrase in msg_phrase:
                            while len(phrase) > LIMIT_SHOW_MSG:
                                if phrase[LIMIT_SHOW_MSG] == " ":
                                    msg_lines.append(phrase[:LIMIT_SHOW_MSG])
                                    phrase = phrase[LIMIT_SHOW_MSG:]
                                else:
                                    if len(phrase.split()) > 1 and len(phrase.split()[0]) < LIMIT_SHOW_MSG:
                                        for e in range(LIMIT_SHOW_MSG, 0, -1):
                                            if phrase[e] == " ":
                                                msg_lines.append(phrase[:e])
                                                phrase = phrase[e + 1:]
                                                break
                                            elif e == 0:
                                                msg_lines.append(phrase[:e])
                                                phrase = phrase[e + 1:]
                                    else:
                                        msg_lines.append(phrase[:LIMIT_SHOW_MSG])
                                        phrase = phrase[LIMIT_SHOW_MSG:]
                                counter += 1
                            lastline = phrase
                            msg = ""
                            msg_lines.append(lastline)
                        # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
                        for i, msg_line in enumerate(msg_lines):
                            if i != len(msg_lines) - 1:
                                msg += msg_line + "\n"
                            else:
                                msg += msg_line
                    print("Inizio secondo Testo\n" + msg + "\nFine secondo Testo")
                    if name:
                        name_label_msg_id = chat_scrolling_area.create_text((0, start_padding) if len(
                            all_showed_msgs_ids) == 0 else (
                            0, chat_scrolling_area.bbox(chat_scrolling_area.find_all()[len(chat_scrolling_area.find_all())-1])[
                                3] + distance_msg_y_position_last_msg),
                                                                            text=name,
                                                                            fill=color_name,
                                                                            font=(font[0], font[1] + 2, font[2]),
                                                                            justify=orientation)

                        print(f"Il nome è: {name}")
                        print(
                            f"Valori generali name:{chat_scrolling_area.coords(name_label_msg_id)}\n\nBbox:{chat_scrolling_area.bbox(name_label_msg_id)}")
                        print(f"NAME id: {name_label_msg_id}")
                    print(f"CHAT SCROLLING: {chat_scrolling_area}")
                    print(f"ITEM ON CHAT SCROLLING: {chat_scrolling_area.find_all()}")
                    msg_show_id = add_to_layer(chat_scrolling_area.create_text, (0, start_padding) if len(
                        all_showed_msgs_ids) == 0 else (
                        0, chat_scrolling_area.bbox(chat_scrolling_area.find_all()[len(chat_scrolling_area.find_all())-1])[
                            3] + distance_msg_y_position_last_msg),
                                               text=msg,
                                               fill=fg,
                                               font=(font[0], font[1], font[2]),
                                               justify=orientation)
                    print(f"Booooool: {len(all_showed_msgs_ids)}")
                    print("Valore asse y: ", (0, start_padding) if len(
                        all_showed_msgs_ids) == 0 else (
                        0, chat_scrolling_area.bbox(all_showed_msgs_ids[len(all_showed_msgs_ids) - 1])[
                            3] + distance_msg_y_position_last_msg))
                    all_showed_msgs_ids.append(msg_show_id)
                    print(f"SHOW id: {msg_show_id}")
                    if show_time:
                        now = datetime.datetime.now()
                        time_label_id = add_to_layer(chat_scrolling_area.create_text, (0, 0),
                                                     text=add_zero(str(now.hour)) + " : " + add_zero(str(now.minute)),
                                                     fill=fg if show_time else "#F7F7F7",
                                                     font=('calibri', 7, 'bold'))
                        print(f"TIME id: {time_label_id}")
                        chat_scrolling_area.tag_bind(time_label_id, "<Button-3>",
                                                     lambda event: copy_msg(event, time_label_id))
                    msg_show_x1 = chat_scrolling_area.bbox(msg_show_id)[0]
                    msg_show_y1 = chat_scrolling_area.bbox(msg_show_id)[1]
                    msg_show_x2 = chat_scrolling_area.bbox(msg_show_id)[2]
                    msg_show_y2 = chat_scrolling_area.bbox(msg_show_id)[3]
                    msg_show_width = msg_show_x2 - msg_show_x1
                    msg_show_height = msg_show_y2 - msg_show_y1
                    print(f"\nAltezza coso label: {msg_show_height}")
                    print(
                        f"\nmsg_show_x1: {msg_show_x1}, msg_show_y1: {msg_show_y1}\nmsg_show_x2: {msg_show_x2}, msg_show_y2: {msg_show_y2}")
                    # 11111111111111111111111222222222222222222222222222233333333333333333333333344444444444444444444555555555555555555555555556666666666666666666666666777777777777777777777788888888888888888888888899999999999999999999990000000000000

                    chat_scrolling_area.update()
                    cos = chat_scrolling_area.bbox(
                        all_showed_msgs_ids[len(all_showed_msgs_ids) - 2])[
                        3]
                    cosb = chat_scrolling_area.itemcget(
                        all_showed_msgs_ids[len(all_showed_msgs_ids) - 2], "text")
                    print(f"EHEE ultimo {cos}\nEHEHEH ultimo labbl {cosb}")
                    print(
                        f"COORDINATE: {chat_scrolling_area.coords(msg_show_id)}, WIDTH: {msg_show_width}, HEIGHT: {msg_show_height}")
                    for i in chat_scrolling_area.find_all():
                        if chat_scrolling_area.bbox(i) != None:
                            print(f"\nBbox on: {i} ---> {chat_scrolling_area.bbox(i)}\n")
                        else:
                            print(f"\nBbox off: {i} ---> {chat_scrolling_area.bbox(i)}\n")
                    if orientation == RIGHT:
                        chat_scrolling_area.yview_moveto("1.0")
                        paddingx = chat_scrolling_area.winfo_width() - msg_show_width / 2 - 30
                        chat_scrolling_area.move(msg_show_id, paddingx, msg_show_height / 2)
                        if show_time:
                            all_showed_msgs_ids.append(time_label_id)
                            chat_scrolling_area.update()
                            chat_scrolling_area.itemconfigure(time_label_id, justify=LEFT)
                            paddingx = chat_scrolling_area.bbox(msg_show_id)[0] - 2
                            print(f"\nBBOX:{chat_scrolling_area.bbox(msg_show_id)}")
                            print(f"\nCOORDINATE: {chat_scrolling_area.coords(msg_show_id)}")
                            chat_scrolling_area.move(time_label_id, paddingx,
                                                     chat_scrolling_area.bbox(msg_show_id)[3] + 5)

                    elif orientation == LEFT:
                        if name:
                            print(f"Tutti i label: {chat_scrolling_area.find_all()}")
                            chat_scrolling_area.update()
                            chat_scrolling_area.update_idletasks()
                            name_label_msg_x1 = chat_scrolling_area.bbox(name_label_msg_id)[0]
                            name_label_msg_y1 = chat_scrolling_area.bbox(name_label_msg_id)[1]
                            name_label_msg_x2 = chat_scrolling_area.bbox(name_label_msg_id)[2]
                            name_label_msg_y2 = chat_scrolling_area.bbox(name_label_msg_id)[3]
                            name_label_msg_width = name_label_msg_x2 - name_label_msg_x1
                            name_label_msg_height = name_label_msg_y2 - name_label_msg_y1
                            all_showed_names_msgs.append(name_label_msg_id)
                            all_showed_msgs_ids.append(name_label_msg_id)
                            chat_scrolling_area.move(name_label_msg_id, name_label_msg_width / 2 - 10,
                                                     name_label_msg_height / 2)
                            chat_scrolling_area.tag_bind(name_label_msg_id, "<Button-3>",
                                                         lambda event: copy_msg(event, name_label_msg_id))
                        chat_scrolling_area.move(msg_show_id, -5 + msg_show_width / 2, msg_show_height / 2)
                        if show_time:
                            all_showed_msgs_ids.append(time_label_id)
                            chat_scrolling_area.itemconfigure(time_label_id, justify=RIGHT)
                            paddingx = chat_scrolling_area.bbox(msg_show_id)[2] + 2
                            chat_scrolling_area.move(time_label_id, paddingx,
                                                     chat_scrolling_area.bbox(msg_show_id)[3] + 5)
                    else:
                        chat_scrolling_area.itemconfigure(msg_show_id, justify=CENTER)
                        paddingx = chat_scrolling_area.winfo_width() / 2
                        print(f"PADDING:{paddingx}, SCROLLING AREA WIDTH:{chat_scrolling_area.winfo_width()}")
                        print(f"LONNNGG: {len(all_showed_msgs_ids)}")
                        print(f"COSO: {all_showed_msgs_ids}")
                        print(f"Last msg center: ",
                              {chat_scrolling_area.bbox(all_showed_msgs_ids[len(all_showed_msgs_ids) - 2])[
                                   3]})
                        chat_scrolling_area.move(msg_show_id, paddingx, msg_show_height / 2)

                    chat_scrolling_area.tag_bind(msg_show_id, "<Button-3>", lambda event: copy_msg(event, msg_show_id))
                    print(
                        f"\nPosizioni successive messaggi: {chat_scrolling_area.coords(msg_show_id)[1]}")

                    chat_scrolling_area.configure(scrollregio=(
                        chat_scrolling_area.bbox("all")[0],
                        chat_scrolling_area.bbox("all")[1],
                        chat_scrolling_area.bbox("all")[2],
                        chat_scrolling_area.bbox("all")[3] + 5))
                    chat_scrolling_area.yview_moveto("1.0")

                    print(f"SHOWED ID: {all_showed_msgs_ids}")
                    print(f"Tutti i msgs: {len(all_showed_msgs_ids)}")
                    return msg

            show_msg(
                "I messaggi sono crittografati end-to-end\nNessuno al di fuori di questa chat può leggerne il contenuto",
                fg="#FFB900", orientation=CENTER, font=('calibri', 10, 'bold'), show_time=False)
            txt = scrolledtext.ScrolledText(bottom_nav, undo=True, bg="white")
            txt['font'] = ('consolas', '12')
            txt.place(width=650, height=95)

            def remove_placeholder(event):
                if get_remove_placeholder_bool():
                    set_remove_placeholder_bool(False)
                    get_str = txt.get('current linestart', 'current lineend+1c').strip()
                    if get_str == "":
                        txt.delete("1.0", "2.0")
                    else:
                        txt.delete('current linestart', 'current lineend+1c')

            txt.insert(1.0, "Scrivi qui il messaggio da inviare")

            def press_key(event):
                remove_placeholder(None)
                if event.char == "\x7f":
                    if not txt.get("current linestart", "insert") == txt.get("current linestart", 1.0):
                        text = txt.get("current linestart", "insert")
                        text_length = len(txt.get(1.0, "insert"))
                        found = False
                        count = 0
                        for char in text:
                            if char == " ":
                                count += 1
                                found = True
                        if count == text_length:
                            found = False
                        if found:
                            for char_n in range(0, text_length, 1):
                                if " " in txt.get("insert -%d chars" % char_n, "insert") and not txt.get(
                                        "insert -%d chars" % char_n, "insert") == " " * char_n:
                                    del_n = char_n - 2
                                    txt.delete("insert -%d chars" % del_n, "insert")
                                    break
                        else:
                            txt.delete('end - 1 lines linestart', 'insert')
                elif event.char == "\n" or (event.char == "\r" and event.state == "Shift"):
                    send(None)

            def no_tab(event):
                return "break"

            def random_color():
                hex_number = ""
                while not len(hex_number) - 1 == 6:
                    random_number = random.randint(0, 16777215)
                    hex_number = format(random_number, 'x')
                    hex_number = '#' + hex_number
                return hex_number

            def send(msg):
                global last_name_client
                if not get_remove_placeholder_bool() or msg == DISCONNECT_MESSAGE:
                    discard = False
                    if msg is None:
                        msg_raw = txt.get("1.0", 'end-1c')

                        """

                        test di invio e ricezione

                        #msg_raw = ""
                        #for i in range(45):
                        msg_raw += f"{i}) Sono il numero {i}\n"

                        """

                        msg = msg_raw.strip()
                    if not msg == "" and not discard:
                        txt.delete("1.0", "end")
                        print("Inizio Testo\n" + msg + "\nFine Test")
                        new_msg = show_msg(msg, fg="#555555", font=('consolas', 12, 'bold'))
                        if not msg == DISCONNECT_MESSAGE:
                            last_name_client = ""
                            print(f"Lunghezza del messaggio: {len(str(len(new_msg)))}.\nHeader: {HEADER}")
                            send_message_to_server_with_check(client, MESSAGE, False)
                            send_message_to_server_with_check(client, new_msg, False)
                            txt.delete("1.0", "end")
                            txt.insert("1.0", "Scrivi qui il messaggio da inviare")
                            set_remove_placeholder_bool(True)
                        else:
                            root.destroy()
                            send_message_to_server_with_check(client, LEFT_CLIENT_MSG)
                            send_message_to_server_with_check(client, REMOVE_CLIENTS_TO_CHAT)
                            send_message_to_server_with_check(client, this_profile[0])
                            send_message_to_server_with_check(client, DISCONNECT_MESSAGE)
                            send_message_to_server_with_check(client, "False")
                            new_client = socket.socket()
                            connect_to(new_client, ADDR)
                            globals()["chat_scrolling_area"] = None
                            send_message_to_server_with_check(new_client, RECONN_MSG)
                            import Client_hub
                            Client_hub.heandle_hub(new_client, ADDR)
                    else:
                        txt.delete("1.0", "end")
                        txt.insert("1.0", "Scrivi qui il messaggio da inviare")
                        set_remove_placeholder_bool(True)

            def disconnect():
                send_message_to_server_with_check(client, PASS_MSG)
                send(DISCONNECT_MESSAGE)

            globals()["all_rooms"] = None
            send_message_to_server_with_check(client, CHAT_ROOMS_MSG_T2)
            root.protocol("WM_DELETE_WINDOW", disconnect)
            globals()["RECV_bool"] = False
            globals()["JOINED_bool"] = False
            globals()["NEW_CLIENT_MSG_bool"] = False
            globals()["MESSAGE_bool"] = False
            globals()["LEFT_CLIENT_MSG_bool"] = False
            globals()["JOINED_recv"] = ""
            globals()["NEW_CLIENT_MSG_recv"] = ""
            globals()["MESSAGE_recv"] = ["", "", "", ""]
            globals()["LEFT_CLIENT_MSG_recv"] = []
            globals()['members'] = None
            clients_name = [[], []]

            def listening():
                global last_name_client, this_room

                print("-----INIZIO ASCOLTO CLIENT --> SERVER-----")
                while True:
                    msg = recv_with_long(client, True)
                    print(f"msg: {msg}")
                    if msg == JOINED:
                        globals()["JOINED_bool"] = True
                        name_client = recv_with_long(client, True)
                        globals()["JOINED_recv"] = name_client + " si è unito alla chat!"
                        print(f"clients_name[0] -> {name_client}")
                        clients_name[0].append(name_client)
                        print(f"clients_name[0] -> {name_client}")
                        clients_name[1].append(random_color())
                        last_name_client = ""
                    elif msg == NEW_CLIENT_MSG:
                        globals()["NEW_CLIENT_MSG_bool"] = True
                        globals()["NEW_CLIENT_MSG_recv"] = recv_with_long(client, True)
                        print(f"Global: {globals()['NEW_CLIENT_MSG_recv']}")
                        last_name_client = ""
                    elif msg == LEFT_CLIENT_MSG:
                        globals()["LEFT_CLIENT_MSG_bool"] = True
                        exited_client = ast.literal_eval(recv_with_long(client, True))
                        last_name_client = ""
                        globals()["LEFT_CLIENT_MSG_recv"] = exited_client
                    elif msg == PASS_MSG:
                        print("Sono uscito dal questo thread --> 2")
                        break
                    elif msg == MESSAGE or msg == END_LONG_MESSAGE:
                        name_client = recv_with_long(client, True)
                        color_name = ""
                        for index, name in enumerate(clients_name[0]):
                            print(f"name for color: {name}")
                            if name == name_client:
                                print(f"colorreeeeee")
                                color_name = clients_name[1][index]
                                break
                        message = recv_with_long(client, True)
                        globals()["MESSAGE_recv"][0] = name_client
                        globals()["MESSAGE_recv"][1] = message
                        globals()["MESSAGE_recv"][2] = last_name_client
                        globals()["MESSAGE_recv"][3] = color_name
                        last_name_client = name_client
                        globals()["MESSAGE_bool"] = True
                    elif msg == INFO_MSG_T2:
                        globals()['members'] = ast.literal_eval(recv_with_long(client, True))
                        print(f"Members: {globals()['members']}")
                        for member in globals()['members']:
                            if member[1] not in clients_name[0] and not member[0] == client.getpeername()[0]:
                                print(f"clients_name[0] -> {member[1]}")
                                clients_name[0].append(member[1])
                                print(f"clients_name[0] -> {member[1]}")
                                clients_name[1].append(random_color())
                    elif msg == CHAT_ROOMS_MSG_T2:
                        globals()["all_rooms"] = ast.literal_eval(recv_with_long(client, True))
                    elif msg == RECV_MSG:
                        print(f"RICEVUTOO: {messages_to_send}")
                        send_message_to_server()
                    else:
                        print(msg)
                        print("Sono uscito dal questo thread --> 2")
                        break
                    globals()["RECV_bool"] = True

            thread = threading.Thread(target=listening)
            thread.setDaemon(True)
            thread.start()

            refresh_remove_placeholder_bool()
            txt.bind("<KeyPress>", press_key)
            txt.bind("<Tab>", no_tab)
            txt.bind("<Button-1>", remove_placeholder)
            submint_button = Button(bottom_nav, text="Invia", font=('calibri', 16, 'bold'))
            submint_button["command"] = partial(send, None)
            submint_button.place(relx=0.835, rely=0.05, width=75, height=30)
            esc_button = Button(bottom_nav, text="Disconnettiti", font=('calibri', 16, 'bold'))
            esc_button["command"] = lambda: disconnect()
            esc_button.place(relx=0.835, rely=0.5, width=125, height=35)
            bottom_nav.place(relx=0.0029, rely=0.851, width=796, height=100)
            globals()['members'] = None
            send_message_to_server_with_check(client, INFO_MSG_T2)
            while globals()['members'] is None:
                print("test1")
                time.sleep(0.05)
                root.update()
            while globals()['all_rooms'] is None:
                print("test2")
                time.sleep(0.05)
                root.update()
                chat_scrolling_area.update()
            gear = PhotoImage(file="img/option.png")
            for room in globals()['all_rooms']:
                if this_profile[0] in room[2]:
                    this_room = room
            print(f"THIS ROOM: {this_room}")
            if this_room[1][0] == "private":
                print("oiii provaaaa")
                configurations.append("Invita")
            config_btn = Button(chat_frame, image=gear, compound=TOP)
            for i, config in enumerate(configurations):
                if isinstance(config, list):
                    print(f"CONFIGURAZIONEEEEEE: {config}")
                    btns_config.append(Button(chat_frame, text=config[0]))
                    btns_config[i].place(x=800, y=i * 25 + 42, width=100)
                    sub_configs_pos = []

                    def sub_configs_header(action, btns, btn):
                        print(f"\n\nNome bottone: {btn}\n\n")
                        go = True
                        for repress_animation_bool in repress_animation_bools:
                            if repress_animation_bool[0] == btn:
                                if repress_animation_bool[3]:
                                    go = False
                                    break
                        if go:
                            forget = []
                            for i in range(len(btns)):
                                forget.append(False)
                            for i, btn in enumerate(btns):
                                if action == "Leave":
                                    print("\n\nFuori")
                                    x_pointer = root.winfo_pointerx() - root.winfo_rootx()
                                    y_pointer = root.winfo_pointery() - root.winfo_rooty()
                                    x_btn_1, y_btn_1, x_btn_2, y_btn_2 = bbox(btn)
                                    print(f"Posizione cursore: {(x_pointer, y_pointer)}")
                                    print(f"Posizione bottone: {(btn.winfo_x(), btn.winfo_y())}")
                                    print(f"Vertici: {bbox(btn)}")
                                    if not (x_btn_1 < x_pointer < x_btn_2 and y_btn_1 < y_pointer < y_btn_2):
                                        print("Fuori ma tanto\n\n")
                                        forget[i] = True

                            if all(flag == True for flag in forget):
                                [btn_.place_forget() for btn_ in btns]
                            else:
                                print("Dentro")
                                [btn_.place(x=sub_configs_pos[i][0], y=sub_configs_pos[i][1],
                                            width=sub_configs_pos[i][2])
                                 for i, btn_ in enumerate(btns)]

                    def show_members():
                        globals()['members'] = None
                        send_message_to_server_with_check(client, INFO_MSG_T2)
                        while globals()['members'] is None:
                            root.update()
                        raise_frame(members_frame)

                        #   NOME ----- ip ----- COLORE ---- SEGNALA #
                        def change_color(event, name_member, item_id):
                            color = askcolor(title="Seleziona un colore")[1]
                            members_scrolling_area.itemconfig(item_id, fill=color)
                            members_scrolling_area.update()
                            print(f"\n\nCLIENTS_COLORS: {clients_name}\n\n")
                            for index, name in enumerate(clients_name[0]):
                                if name == name_member:
                                    clients_name[1][index] = color
                                    break
                            for name_msg_id in all_showed_names_msgs:
                                if chat_scrolling_area.itemcget(name_msg_id, "text") == name_member:
                                    chat_scrolling_area.itemconfigure(name_msg_id, fill=color)
                            chat_scrolling_area.update()
                            root.update()

                        def report_action():
                            pass

                        def show_clients(members):
                            for i, member in enumerate(members):
                                place_object(members_scrolling_area, members_scrolling_area.create_text,
                                             (60, 50 + 50 * i),
                                             text=member[1],
                                             fill="#555555",
                                             font=('calibri', 14, 'bold') if OS == "Windows" else ('calibri', 14),
                                             justify="left")
                                ip_label = place_object(members_scrolling_area, members_scrolling_area.create_text,
                                                        (300, 50 + 50 * i),
                                                        text=member[0],
                                                        fill="#555555",
                                                        font=('calibri', 14, 'bold') if OS == "Windows" else (
                                                            'calibri', 14),
                                                        justify="left")

                                # if member[0] != client.getsockname()[0]:
                                color_name = ""
                                for index, name in enumerate(clients_name[0]):
                                    if name == member[1]:
                                        color_name = clients_name[1][index]
                                        break
                                print(f"COso maggiore label ip:{members_scrolling_area.bbox(ip_label)}")
                                color_btn = place_object(members_scrolling_area,
                                                         members_scrolling_area.create_rectangle,
                                                         (470, members_scrolling_area.bbox(ip_label)[1] - 10, 500,
                                                          members_scrolling_area.bbox(ip_label)[3] - 12),
                                                         fill=color_name,
                                                         outline="grey60")
                                members_scrolling_area.tag_bind(color_btn, "<Button-1>",
                                                                lambda event: change_color(event, member[1],
                                                                                           color_btn))
                                report_str = place_object(members_scrolling_area, members_scrolling_area.create_text,
                                                          (600, 50 + 50 * i), text="SEGNALA",
                                                          font=("calibri", 14, 'bold'),
                                                          fill="#555555",
                                                          tags="report_label_" + str(i))
                                report_rct = place_object(members_scrolling_area,
                                                          members_scrolling_area.create_rectangle,
                                                          (members_scrolling_area.bbox(report_str)[0] - 50 - abs(
                                                              members_scrolling_area.bbox(report_str)[2] -
                                                              members_scrolling_area.bbox(report_str)[0]) / 2,
                                                           members_scrolling_area.bbox(report_str)[1] - 5 - abs(
                                                               members_scrolling_area.bbox(report_str)[3] -
                                                               members_scrolling_area.bbox(report_str)[1]) / 2,
                                                           members_scrolling_area.bbox(report_str)[2] - abs(
                                                               members_scrolling_area.bbox(report_str)[2] -
                                                               members_scrolling_area.bbox(report_str)[0]) / 2,
                                                           members_scrolling_area.bbox(report_str)[3] - abs(
                                                               members_scrolling_area.bbox(report_str)[3] -
                                                               members_scrolling_area.bbox(report_str)[1]) / 2
                                                           ), fill="#900000",
                                                          outline="#000000",
                                                          width=2,
                                                          tags="report_label_" + str(
                                                              i))  # (500, 32.5 + 25 * i, 650, 57.5 + 25 * i)

                                def hover(event, tag, type):
                                    print(event)
                                    objs = members_scrolling_area.find_withtag(tag)
                                    print(f"\nTipologia: {type}\n")
                                    print(
                                        f"\nHover objs id: {objs}\nHover obj tags:{tag}\n")
                                    if type == "Enter":
                                        members_scrolling_area.itemconfigure(objs[1], fill="#FFFFFF")
                                        members_scrolling_area.itemconfigure(objs[0], fill="#FF0000")
                                    else:
                                        members_scrolling_area.itemconfigure(objs[1], fill="#555555")
                                        members_scrolling_area.itemconfigure(objs[0], fill="#900000")

                                print(f"Valori id label report:\nstringa: {report_str}\nrettangolo: {report_rct}")
                                members_scrolling_area.tag_bind("report_label_" + str(i), "<ButtonPress-1>",
                                                                lambda event, tag="report_label_" + str(i): hover(event,
                                                                                                                  tag,
                                                                                                                  "Enter"))
                                members_scrolling_area.tag_bind("report_label_" + str(i), "<ButtonRelease-1>",
                                                                lambda event, tag="report_label_" + str(i): hover(event,
                                                                                                                  tag,
                                                                                                                  "Leave"))
                                members_scrolling_area.tag_lower(report_rct, report_str)
                                members_scrolling_area.update()

                        def sort():
                            infos_sorted = []
                            members_ = members[:]
                            for member in members_:
                                infos_sorted.append(member[1])
                            new_infos_sorted = []
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

                            for e in range(len(numbers_str) - 1):
                                if numbers_str[e][0] > numbers_str[e + 1][0]:
                                    temp = numbers_str[e + 1]
                                    numbers_str[e + 1] = numbers_str[e]
                                    numbers_str[e] = temp

                            print(f"Numeri ordinati: {numbers_str}\nStringhe ordinate: {strs}")
                            new_infos_sorted_str = []
                            [new_infos_sorted_str.append(number[1]) for number in numbers_str]
                            new_infos_sorted_str.extend(strs)
                            for names in new_infos_sorted_str:
                                for i, info in enumerate(members_):
                                    if info[1][1] == names:
                                        del (members_[i])
                                        new_infos_sorted.append(info)
                                        break
                            return new_infos_sorted

                        def change_state(btn, state, imgs):
                            global remove, order
                            if state == 1:
                                btn["image"] = imgs[1]
                                btn["command"] = lambda new_state=0: change_state(btn, new_state, imgs)
                                show_clients(sort())
                            else:
                                btn["image"] = imgs[0]
                                btn["command"] = lambda new_state=1: change_state(btn, new_state, imgs)
                                show_clients(globals()['members'])

                        arrow_imgs = ["img/uparrow.png", "img/downarrow.png"]
                        imgs = []
                        for img in arrow_imgs:
                            img_a = PhotoImage(file=img)
                            img_b = img_a.subsample(1, 1)
                            imgs.append(img_b)
                        p = Button(members_frame, text="Nome", compound=TOP,
                                   borderwidth=0, relief=SUNKEN, font=('calibri', 12, 'bold'),
                                   fg="#646464", image=imgs[0])
                        p["command"] = lambda: change_state(p, 1, imgs)
                        p.place(x=60, y=15)
                        members_scrolling_area = Canvas(members_frame, bd=1, relief="solid")
                        members_scrolling_area.config(scrollregion=members_scrolling_area.bbox("all"))
                        members_scrolling_area.place(x=1, y=50, width=798, height=600)
                        members_scr = Scrollbar(members_scrolling_area)
                        members_scrolling_area.config(yscrollcommand=members_scr.set)
                        members_scr.config(command=members_scrolling_area.yview)
                        if OS == "Linux":
                            members_scrolling_area.bind("<Button-4>",
                                                        lambda event: scroll_event(event, members_scrolling_area, 1))
                            members_scrolling_area.bind("<Button-5>",
                                                        lambda event: scroll_event(event, members_scrolling_area, -1))
                        else:
                            members_scrolling_area.bind("<MouseWheel>",
                                                        lambda event: scroll_event(event, members_scrolling_area))
                        members = globals()['members']
                        show_clients(members)
                        members_scrolling_area.configure(scrollregio=(
                            members_scrolling_area.bbox("all")[0],
                            members_scrolling_area.bbox("all")[1],
                            members_scrolling_area.bbox("all")[2],
                            members_scrolling_area.bbox("all")[3] + 5))
                        Button(members_frame, text="Indietro", font=('calibri', 12, 'bold'),
                               command=lambda: raise_frame(chat_frame)).place(x=798 / 2 - 25, y=660)

                    def report_chat():

                        pass

                    def leave_chat():

                        pass

                    functions = [show_members, report_chat, leave_chat]
                    for e in range(len(config) - 1):
                        print(f"CONFIGURAZIONEEEEEE: {config[e + 1]}")
                        btns_sub_configs.append(Button(chat_frame, text=config[e + 1], command=functions[e]))
                        sub_configs_pos.append([574, e * 25 + i * 25 + 42, 100])

                    for j in range(len(config) - 1):
                        btns_sub_configs[j].bind("<Enter>", lambda event: sub_configs_header("Enter", btns_sub_configs[
                                                                                                      e - (
                                                                                                              len(config) - 1):e + 1],
                                                                                             config_btn))
                        btns_sub_configs[j].bind("<Leave>", lambda event: sub_configs_header("Leave", btns_sub_configs[
                                                                                                      e - (
                                                                                                              len(config) - 1):e + 1],
                                                                                             config_btn))

                    btns_config[i].bind("<Enter>", lambda event: sub_configs_header("Enter", btns_sub_configs[
                                                                                             e - (
                                                                                                     len(config) - 1):e + 1],
                                                                                    config_btn))
                    btns_config[i].bind("<Leave>", lambda event: sub_configs_header("Leave", btns_sub_configs[
                                                                                             e - (
                                                                                                     len(config) - 1):e + 1],
                                                                                    config_btn))
                else:
                    btns_config.append(Button(chat_frame, text=config))
                    btns_config[i].place(x=800, y=i * 25 + 42, width=100)

            config_btn["command"] = lambda: set_animenation_variables(chat_frame, btns_config, "options", 10,
                                                                      pos=[[674, 42]],  # [674, 42]
                                                                      time_of_single_animation=0.02,
                                                                      position_repress=[[800, 42]],
                                                                      # [800, 42]
                                                                      btn_object=config_btn)
            config_btn.place(x=743, y=10)
            esc_button.update()
            submint_button.update()
            while True:
                if globals()["JOINED_bool"]:
                    globals()["JOINED_bool"] = False
                    show_msg(globals()["JOINED_recv"], fg="#123456", orientation=CENTER,
                             font=('calibri', 12, 'bold'), show_time=False)
                elif globals()["CHAT_CREATED_bool"]:
                    globals()["CHAT_CREATED_bool"] = False
                    show_msg(globals()["CHAT_CREATED_str"], fg="#123456", orientation=CENTER,
                             font=('calibri', 12, 'bold'), show_time=False)
                elif globals()["NEW_CLIENT_MSG_bool"]:
                    globals()["NEW_CLIENT_MSG_bool"] = False
                    show_msg(globals()["NEW_CLIENT_MSG_recv"], fg="#123456", orientation=CENTER,
                             font=('calibri', 12, 'bold'), show_time=False)
                elif globals()["MESSAGE_bool"]:
                    globals()["MESSAGE_bool"] = False
                    name_client = globals()["MESSAGE_recv"][0]
                    message = globals()["MESSAGE_recv"][1]
                    last_name_client = globals()["MESSAGE_recv"][2]
                    color_name = globals()["MESSAGE_recv"][3]
                    print(f"Colore ricevente: {color_name}")
                    if not last_name_client == name_client:
                        show_msg(message, name=name_client, fg="#123456", orientation=LEFT,
                                 font=('consolas', 13, 'bold'), color_name=color_name)
                    else:
                        show_msg(message, name=None, fg="#123456", orientation=LEFT,
                                 font=('consolas', 13, 'bold'), color_name=color_name, padding=False)
                elif globals()["LEFT_CLIENT_MSG_bool"]:
                    globals()["LEFT_CLIENT_MSG_bool"] = False
                    show_msg(f"{globals()['LEFT_CLIENT_MSG_recv'][1]} si è disconnesso!", fg="#123456",
                             orientation=CENTER,
                             font=('calibri', 12, 'bold'), show_time=False)
                chat_frame.update_idletasks()
                chat_frame.update()
                members_frame.update_idletasks()
                members_frame.update()
                time.sleep(0.08)

        thread_gui = threading.Thread(target=gui)
        thread_gui.setDaemon(False)
        thread_gui.start()

    def add_zero(string):
        if len(string) == 1:
            string_out = "0" + string
        else:
            string_out = string
        return string_out
