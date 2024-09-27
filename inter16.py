import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, Menu, scrolledtext
from tkinter import filedialog as fd
import ttkbootstrap as boottk
from ttkbootstrap.constants import *
import datetime
import analize01 as ana_cisco
import analize02 as ana_juniper
import enc01 as enc
import gemini as gem
import env01 as env
import os
import time
import threading
import subprocess
import re
import paramiko
from datetime import datetime
from dotenv import load_dotenv
import random


#load .env
load_dotenv()

file_name = "script.txt"
analisys_file = "analisys.txt"
srun_file = "configuration.txt"
theme_file = "tfile.txt"
arp_file = "arp.txt"
host_remember = "host_remember.txt"
version_file = "version.txt"
interfaces_file = "interface.txt"
routes_file = "routes.txt"
arp_file = "arp.txt"
dinamic_file = "dinamic.txt"
interface_conf_file = "interface_conf_file.txt"
vrf_file = "vrf.txt"
afiles_list = [file_name, srun_file, analisys_file, version_file, interfaces_file, routes_file, arp_file, dinamic_file, interface_conf_file, vrf_file]

cmd00 = "terminal length 0\n"
cmd01 = "show ip route static\n"
cmd011 = "show ip route bgp\n"
cmd012 = "show ip route eigrp\n"
cmd02 = "show ip inter br\n"
cmd03 = "show clock\n"
cmd04 = "show ip arp\n"
cmd05 = "show run\n"
cmd06 = "show version\n"
cmd07 = "show ip vrf\n"

cmdj00 = "cli\n"
cmdj01 = "show route table inet\n"
cmdj02 = "show interface terse | no-more\n"
cmdj04 = "show arp no-resolve\n"
cmdj05 = "show configuration | display set | no-more\n"
cmdj06 = "show version | no-more\n"
cmdj07 = "show system uptime\n"
cmdj08 = "show configuration routing-instance | display set | no-more\n"
cmd0j9 = "show configuration interface | display set | no-more\n"

cmds_list_cisco = [cmd06, cmd05, cmd04, cmd07, cmd01, cmd011, cmd012, cmd02]
cmds_list_juniper = [cmd0j9, cmdj05, cmdj06, cmdj08, cmdj07, cmdj01, cmdj02, cmdj04]

background_colors_list = ["deepskyblue", "darkslategray1", "darkseagreen1",
 "cornsilk", "lavender", "lightcyan1", "lightgoldenrodyellow", "lightsalmon1",
 "lightskyblue", "mintcream", "powderblue", "seashell2", "sgilightblue", "whitesmoke"]
host_detail_list = []
host_list = []
new_list = []
counter = 0
ana_counter = 0
unable_counter = 0
cterminal_couter = 0
#item in hosts combox01
item_chosen = ""
b_width = 25
entry_width = 15
lpady = 7
theme_x = 0
my_theme = os.getenv("main_theme")
fsize = int(os.getenv("main_windows_font_size"))
ffont = os.getenv("main_windows_font")
main_fsize = 8
main_font = "MS Sans Serif"
response_time = float(os.getenv("response_time"))
button_style = "Outline.TButton"
combox_style = "info.TCombobox"

with open(file_name, "w") as file:
    file.write("")
with open(srun_file, "w") as file:
    file.write("")

def write_file(output):
    with open(file_name, "a") as file:
        file.write(f"{output}\n")
        file.write(f"#\n")

def show_ana(button):
    answers.delete("1.0", tk.END)
    match button:
        case 1:
            with open(interfaces_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")
                answers.see(tk.END)
        case 2:
            with open(routes_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")
        case 3:
            with open(arp_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")
        case 4:
            with open(dinamic_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")
        case 5:
            with open(version_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")
        case 6:
            with open(interface_conf_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")
        case 7:
            with open(vrf_file, "r") as file:
                answers.insert(tk.END, f"{combo_box01.get()} - {file.read()}\n")

def analize_run():
    ana_butt_disable()
    #checkbocks01 - Remember Me - for host details. if 'ON' go to function to add host
    if checkbutton01_var.get() == 1:
        remember_me()
    with open(file_name, 'w') as file:
        file.write("")
    if combo_box01.get() !="" and entry02.get() !="" and entry03.get() !="":
        answers.delete("1.0", tk.END)
        thread01 = threading.Thread(target=run_cmd)
        thread01.start()
        thread02 = threading.Thread(target=check_pings)
        thread02.start()
    else:
        answers.insert(tk.END, "Enter IP/Username/Password\n")

def run_cmd():
    port = os.getenv("port")
    vendure = combo_box02.get()
    if vendure == "Cisco":
        cmds = cmds_list_cisco
    elif vendure == "Juniper":
        cmds = cmds_list_juniper
    ssh_succedd = False
    global ana_counter
    answers.insert(tk.END, f"{combo_box01.get()} - Collecting Data\n")
    try:
        ssh_client01 =paramiko.SSHClient()
        ssh_client01.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client01.connect(combo_box01.get() , port, entry02.get(), entry03.get())
        channel = ssh_client01.invoke_shell()
        output = channel.recv(9999)
        if output.decode("ascii")[-1] == ">" and vendure == "Cisco":
            channel.send("enable\n")
            time.sleep(1)
            stop_key = "password"
            output =  channel.recv(9999)
            stop_key = re.search(r"Password", output.decode("ascii"))
            if stop_key:
                print("Password Line")
                pass_entry_win()
                global en_pass
                en_pass = None
                while True:
                    if en_pass:
                        channel.send(f"{en_pass}\n")
                        time.sleep(1)
                        output = channel.recv(9999)
                        if output.decode("ascii")[-1] == "#":
                            login_succedd = True
                        break

        if vendure == "Cisco":
            channel.send("terminal length 0\n")
            if output.decode("ascii")[-1] == "#":
                ssh_succedd = True
        elif vendure == "Juniper":
            channel.send("cli\n")
            time.sleep(response_time + 2)
            if channel.recv_ready():
                output = channel.recv(9999)
                print(output.decode("ascii"))
            if ">" in output.decode("ascii"):
                ssh_succedd = True
                login_succedd = True
    except Exception as e:
        answers.insert("1.0", f"\n!!!!!!!!!!!!!!!!!!!\n{e}\n")
        ssh_succedd = False

    if ssh_succedd and login_succedd:
        for cmd in cmds:
            ana_counter +=1
            #first 3 commands, I gave higher response_time. then go faster
            if ana_counter <=3:
                time_sleep = response_time + 1
            else:
                time_sleep = response_time
            channel.send(cmd)
            time.sleep(time_sleep)
            if channel.recv_ready():
                output = channel.recv(5000)
                if cmd == cmd05 or cmd == cmdj05:
                    time.sleep(2)
                    with open(srun_file, "w") as file:
                        file.write(output.decode("ascii"))
                write_file(output.decode("ascii"))
            answers.insert(tk.END, f"\nData Ready - {cmd}\n")

        if vendure == "Cisco":
            ana_cisco.run_it()
        elif vendure == "Juniper":
            ana_juniper.run_it()
        ana_butt_enable()
        ssh_client01.close()
    else:
        answers.insert(tk.END, "Can't analize")

    #enable buttons after collecting the data they need


def send_pass(event, pass_win, entry_pass):
    global en_pass
    en_pass = entry_pass.get()
    pass_win.destroy()

def pass_entry_win():
    global entry_pass
    pass_win = Toplevel(window)
    label_pass = Label(pass_win, text="Enter Enable Password", width="20", justify='left', font=(main_font, main_fsize))
    entry_pass = Entry(pass_win, width="20", show="*")
    entry_pass.bind('<Return>', lambda event:send_pass(event, pass_win, entry_pass))
    label_pass.pack()
    entry_pass.pack()

def check_ping():
    answers.delete("1.0", tk.END)
    host = combo_box01.get()
    p = subprocess.Popen(["ping", host], stdout=subprocess.PIPE)
    out = p.stdout.read().decode('ascii')
    answers.delete("1.0", tk.END)
    answers.insert(tk.END, out)

def check_ping_tread():
    if combo_box01.get() !="":
        x = threading.Thread(target=check_ping)
        x.start()

def terminal(terminal_text):
    remember_me()
    port = os.getenv("port")
    terminal_fsize = int(os.getenv("font_size"))
    terminal_font = os.getenv("font")
    response_time = float(os.getenv("response_time"))
    try:
        if combo_box01.get() !="" or entry02.get() !="" or entry03.get() !="":
            ssh_client02 =paramiko.SSHClient()
            ssh_client02.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client02.connect(combo_box01.get() , port, entry02.get(), entry03.get())
            channel = ssh_client02.invoke_shell()
            output05 = channel.recv(9999)
            #disable --More-- function - Cisco
            if combo_box02.get() == "Cisco":
                channel.send("terminal length 0\nterminal shell\n")
            elif combo_box02.get() == "Juniper":
                channel.send("\n\ncli\n")
            top = Toplevel(window)
            size_position = os.getenv("top_size_position")
            top.geometry(size_position)
            top.protocol("WM_DELETE_WINDOW", (lambda : on_terminal_close(top, ssh_client02, answers05)))
            top.title(f"{combo_box01.get()} - Terminal")
            menubar = Menu(top)
            filemenu = Menu(menubar, tearoff=0)
            settings_menu = Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Commands", menu=filemenu)
            menubar.add_cascade(label="Settings", menu=settings_menu)
            if combo_box02.get() == "Cisco":
                to_find01 = "submenu"
                to_find02 = "#"
                counter = -1
                with open("cisco_menu.txt", "r") as file:
                    cisco_menu = file.readlines()
                    for item in cisco_menu:
                        counter +=1
                        counter01 = 1
                        if to_find01 in item:
                            found_line = counter
                            globals()[item.rstrip()] = Menu(filemenu)
                            filemenu.add_cascade(label=cisco_menu[found_line+1].rstrip(), menu=globals()[item.rstrip()], underline=0)
                            for cmd in cisco_menu[found_line+2:]:
                                if to_find02 in cmd:
                                    break
                                elif counter01 < 1:
                                    counter01 +=1
                                    continue
                                else:
                                    globals()[item.rstrip()].add_command(label=cmd.rstrip(), command = lambda x=cmd: pop_cmd(True, answers05, entry05, x, channel))
                                    counter01 += 1

            elif combo_box02.get() == "Juniper":
                to_find01 = "submenu"
                to_find02 = "#"
                counter = -1
                with open("juniper_menu.txt", "r") as file:
                    juniper_menu = file.readlines()
                    for item in juniper_menu:
                        counter +=1
                        counter01 = 1
                        if to_find01 in item:
                            found_line = counter
                            globals()[item.rstrip()] = Menu(filemenu)
                            filemenu.add_cascade(label=juniper_menu[found_line+1].rstrip(), menu=globals()[item.rstrip()], underline=0)
                            for cmd in juniper_menu[found_line+2:]:
                                if to_find02 in cmd:
                                    break
                                elif counter01 < 1:
                                    counter01 +=1
                                    continue
                                else:
                                    globals()[item.rstrip()].add_command(label=cmd.rstrip(), command = lambda x=cmd: pop_cmd(True, answers05, entry05, x, channel))
                                    counter01 += 1

            sub_menu01 = Menu(settings_menu, tearoff=0)
            settings_menu.add_cascade(label="Choose Terminal Font", menu=sub_menu01, underline=0)
            with open("fonts.txt", "r") as file:
                fonts_list = file.readlines()
            for item in fonts_list:
                sub_menu01.add_command(label=item.rstrip(), command = lambda x = item.rstrip() : change_font(x, top, ssh_client02, answers05))

            sub_menu02 = Menu(settings_menu, tearoff=0)
            settings_menu.add_cascade(label="Choose Font Size", menu=sub_menu02, underline=0)
            for item in range(7,15):
                sub_menu02.add_command(label=item, command = lambda x = item : change_size(x, top, ssh_client02, answers05))
            settings_menu.add_command(label = "Load Default Settings", command = lambda: load_default_settings(top, ssh_client02, answers05))
            top.config(menu=menubar)
            answers05 = boottk.Text(top, wrap=WORD, font=(terminal_font, terminal_fsize))
            answers05.pack(fill="both", expand=True)
            answers05.insert("1.0", f"{output05.decode("ascii")}{terminal_text}")
            answers05.see(boottk.END)
            entry05 = boottk.Entry(top, justify='left', width=62)
            entry05.pack(fill="both", expand=False)
            entry05.bind('<Return>', lambda event: pop_cmd(None, answers05, entry05, entry05.get(), channel))
        else:
            answers.insert(tk.END, "Enter IP/Username/Password\n")

    except Exception as e:
        answers.insert("1.0", f"\n!!!!!!!!!!!!!!!!!!!\n{e}\n")

def on_terminal_close(top, ssh_client02, answers05, default_position=False):
    size_position = top.winfo_geometry()
    #wait for final postion/last font/last size to save to env.
    #if False remember final postion
    #if True go back to default position
    if default_position == False:
        env.chenge_var("top_size_position", str(size_position))
    ssh_client02.close()
    top.destroy()


def change_font(font_ch, top, ssh_client02, answers05):
    os.environ["font"] = font_ch
    env.chenge_var("font", font_ch)
    reload_terminal(top, ssh_client02, answers05)

def change_size(size_ch, top, ssh_client02, answers05):
    os.environ["font_size"] = str(size_ch)
    env.chenge_var("font_size", str(size_ch))
    #for font/size change to be visble, reload the window
    reload_terminal(top, ssh_client02, answers05, False)

def reload_terminal(top, ssh_client02, answers05, default_position=False):
    #get the text from widget before destroy
    #so I can desplay it on reloaded window
    terminal_text = answers05.get("1.0", boottk.END)
    #close the top window, and open again with the new font/size values
    on_terminal_close(top, ssh_client02, answers05, default_position)
    terminal(terminal_text)

def load_default_settings(top, ssh_client02, answers05):
    #load from .env default values
    default_font = os.getenv("default_font")
    default_fsize = os.getenv("default_fsize")
    default_size_position = os.getenv("default_top_size_position")
    #set value into windows env
    os.environ["font"] = default_font
    #save values into .env file
    env.chenge_var("font", default_font)
    os.environ["font_size"] = default_fsize
    env.chenge_var("font_size", default_fsize)
    os.environ["top_size_position"] = default_size_position
    env.chenge_var("top_size_position", default_size_position)

    reload_terminal(top, ssh_client02, answers05, True)

def on_app_close():
    for item in afiles_list:
        try:
            os.remove(item)
        except:
            pass
    env.delete_env()
    window.destroy()

def on_resize(event, top):
    size_position = top.winfo_geometry()
    os.environ["top_size_position"] = size_position

def pop_cmd(event, answers05, entry05, entry_cmd, channel):
    #sent command to ssh host using shell
    print(entry_cmd)
    if entry_cmd.rstrip() == "break":
        channel.send("\x03")
    else:
        channel.send(f"{entry_cmd}\n")
    #delay 'response_time' seconds, if network slow, can be increased
    if "show run" in entry_cmd:
        response_time01 = 1
    else:
        response_time01 = 0.2
    time.sleep(response_time01)
    if channel.recv_ready():
        #get host respond (binary text)
        output05 = channel.recv(5000)
        answers05.insert(boottk.END, f"{output05.decode("ascii")}\n")
        answers05.see(boottk.END)
        entry05.delete(0, 'end')
    else:
        answers05.insert("1.0", f"Something Wrong. Check SSH Conection")

def ana_butt_enable():
    button11.configure(state="enable")
    button12.configure(state="enable")
    button13.configure(state="enable")
    button14.configure(state="enable")
    button15.configure(state="enable")
    button16.configure(state="enable")
    button17.configure(state="enable")
    button18.configure(state="enable")
    button19.configure(state="enable")

def ana_butt_disable():
    button11.configure(state="disable")
    button12.configure(state="disable")
    button13.configure(state="disable")
    button14.configure(state="disable")
    button15.configure(state="disable")
    button16.configure(state="disable")
    button17.configure(state="disable")
    button18.configure(state="disable")
    button19.configure(state="disable")

def check_pings():
    time.sleep(25)
    fsize = os.getenv("font_size")
    port = os.getenv("port")
    #open ssh socket
    ssh_client03 =paramiko.SSHClient()
    ssh_client03.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client03.connect(combo_box01.get() , port, entry02.get(), entry03.get())
    #create shell
    channel = ssh_client03.invoke_shell()
    time.sleep(1)
    pings_top = Toplevel(window)
    pings_top.title(f"{combo_box01.get()} - Ping's Window")
    answers08 = boottk.Text(pings_top, width=75,  height=25, font=(ffont, fsize))
    answers08.grid(pady=20, padx=20)
    answers08.insert(boottk.END, "Ping to IP's found in arp table\n")
    if combo_box02.get() == "Cisco":
        for item in ips_arp_file():
        #sent command to ssh host using shell
            channel.send(f"{item}\n")
            time.sleep(12)
            if channel.recv_ready():
                output07 = channel.recv(5000)
                find_ms = re.search(r"round-trip min/avg/max = \d+\/\d+\/\d+ ms", output07.decode("ascii"))
                if find_ms:
                    print(find_ms.group())
                find_rate = re.search(r"Success rate is (\b[0-9]?[0-9]\b|100)", output07.decode("ascii"))
                rate = int(find_rate.group().split()[-1])
                if find_rate and find_ms:
                    if rate == 100:
                        bk_color = "chartreuse1"
                        answers08.tag_config(bk_color, background="chartreuse1", foreground="black")
                    elif rate < 100 and rate >= 50:
                        bk_color = "gray80"
                        answers08.tag_config(bk_color, background="gray80", foreground="black")
                    elif rate == 25:
                        bk_color = "darkorange"
                        answers08.tag_config(bk_color, background="darkorange", foreground="black")
                    elif rate == 0:
                        bk_color = "firebrick1"
                        answers08.tag_config(bk_color, background="firebrick1", foreground="black")
                    answers08.insert(boottk.END, f"{item} - {find_rate.group()} - {find_ms.group()}\n", bk_color)
                else:
                    continue
            else:
                continue
    elif combo_box02.get() == "Juniper":
        channel.send("cli\n")
        time.sleep(response_time)
        for item in ips_arp_file():
            #sent command to ssh host using shell
            channel.send(f"{item}\n")
            time.sleep(6)
            channel.send("\x03")
            time.sleep(response_time)
            channel.send("\x03")
            if channel.recv_ready():
                output08 = channel.recv(5000)
                find_text = "statistics"
                output_list = output08.decode("ascii").split()
                if find_text in output_list:
                    find_statistic = output_list.index("statistics")
                    text = ""
                    for output_item in output_list[find_statistic-2:find_statistic+11]:
                        text += f"{output_item} "
                    if output_list[find_statistic+8] == "0%":
                        bk_color = "chartreuse1"
                        answers08.tag_config(bk_color, background="chartreuse1", foreground="black")
                    else:
                        bk_color = "darkorange"
                        answers08.tag_config(bk_color, background="darkorange", foreground="black")
                    answers08.insert(boottk.END, f"{text}\n", bk_color)
                    answers08.see(tk.END)


    answers08.insert(boottk.END, "Done")
    ssh_client03.close()

def ips_arp_file():
    ping_cmd_list = []
    ips_in_arp = []
    lines_counter = 0
    with open(arp_file, "r") as ip_file:
        arp_line = ip_file.readlines()
    for item in arp_line:
        lines_counter +=1
            #fisrt line in arp file is irralavant, so 'for loop' will skip it
        if lines_counter > 2 and item != "\n":
            arp_line_list = item.split()
            ping_cmd = f"ping {arp_line_list[2]}"
            if combo_box02.get() == "Cisco":
                ping_cmd_list.append(ping_cmd)
            ips_in_arp.append(arp_line_list[2])

    temp_ip_list = ips_in_arp.copy()
    if combo_box02.get() == "Juniper":
        with open(vrf_file, "r") as file:
            lines = file.readlines()
            for ip in ips_in_arp:
                for line in lines:
                    find_ip = re.search(ip, line)
                    if find_ip:
                        line_list = line.split()
                        ping_cmd = f"ping routing-instance {line_list[2]} {ip}"
                        ping_cmd_list.append(ping_cmd)
                        #remove from ip list ips that need 'routing instance' for ping
                        temp_ip_list.remove(ip)
            #if ip's remane in list that not include in 'routung instace',
            #ping those example 'ping 192.168.1.1'
            if len(temp_ip_list) > 0:
                for ip in temp_ip_list:
                    ping_cmd = f"ping {ip}"
                    ping_cmd_list.append(ping_cmd)
    return ping_cmd_list

def remember_me():
    global host_detail_list
    counter_rem = 0
    if combo_box01.get() !="" and entry02.get() !="" and entry03.get() !="":
        #create list to compare against preavios hosts list
        host_listx = [combo_box01.get(), entry02.get(), entry03.get()]
        with open(host_remember, "a") as host_remember_file:
            host_remember_file.write(f"{combo_box01.get()} {entry02.get()} {enc.enc_pass(entry03.get())} {combo_box02.get()} {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n")
    read_host_file()

def clear_host_file():
    with open(host_remember, "w") as host_remember_file:
        host_remember_file.write("")
    #create fresh 'host_list[]' & 'host_detail_list[]'
    host_list = []
    host_detail_list = []
    combo_box01.set("")
    entry02.delete(0, 'end')
    entry03.delete(0, 'end')
    #create new encryption key
    enc.key_write()

#combo_box function
def check_input(event):
    global item_chosen
    global host_list
    global host_detail_list
    global new_list

    value = event.widget.get()
    if value == '' or value == item_chosen:
        combo_box01['values'] = host_list
    else:
        data = []
        for item in new_list:
            if value.lower() in item[0].lower():
                item_index = new_list.index(item)
                item_chosen = item[0]
                combo_box01['values'] = host_list
                if len(new_list) > 0:
                    entry02.delete(0, 'end')
                    entry02.insert(0, new_list[item_index][1])
                if len(host_detail_list) > 0:
                    entry03.delete(0, 'end')
                    entry03.insert(0, new_list[item_index][2])
                if len(host_detail_list) > 0:
                    if new_list[item_index][3] == "Cisco":
                        combo_box02.current(0)
                    elif new_list[item_index][3] == "Juniper":
                        combo_box02.current(1)
def read_host_file():
    global new_list
    global host_list
    counter = 0
    host_list = []
    done_hosts = []
    host_detail_list = []

    with open(host_remember, "r") as host_remember_file:
          hosts = host_remember_file.readlines()
          for line in hosts:
              items = line.split()
              if items:
                  host_detail_list.append(items)
                  host_list.append(items[0])
    host_list.reverse()
    if len(host_list) > 0:
        new_list = []
        for host in host_detail_list:
            temp_list = []
            counter = 0
            for item in host:
                if counter == 2:
                    this_password = enc.dec_pass(item[1:-1])
                    temp_list.append(this_password)
                    counter +=1
                else:
                    temp_list.append(item)
                    counter+=1
            new_list.append(temp_list)

def delete_host_duplicates():
        global new_list
        global host_list
        host_list = []
        done_hosts = []
        with open(host_remember, "r") as host_remember_file:
              hosts = host_remember_file.readlines()
              for line in hosts:
                  items = line.split()
                  if items:
                      host_detail_list.append(items)
                      host_list.append(items[0])
        host_detail_list.reverse()

        with open(host_remember, "w") as host_remember_file:
            host_remember_file.write("")

        with open(host_remember, "w") as host_remember_file:
            for item in host_detail_list:
                if item[0] not in done_hosts:
                    new_list.append(item)
                    done_hosts.append(item[0])
                    host_remember_file.write(f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]}\n")

def change_theme(x):
    #theme frame open - theme_x 1,3,5 - Not Even
    #theme frame close - theme 0,2,4 - even
    global theme_x
    theme_x +=1

    def close_options():
        global frame04
        frame04.destroy()
    #if theme frame already open (theme_x = even), do not open it again
    if theme_x % 2 != 0:
        global frame04
        frame04 = boottk.Frame(window)
        frame04.grid(row = 0, column = 0, columnspan = 2)
        my_themes = window.style.theme_names()
        # List of available themes
        my_str = boottk.StringVar(value=window.style.theme_use())  # default selection of theme

        r, c = 0, 0  # row=0 and column =0
        for values in my_themes:  # List of available themes
            b = boottk.Radiobutton(
                frame04, text=values, variable=my_str, value=values, command=lambda: my_upd()
            )  # Radio buttons with themes as values
            b.grid(row=r, column=c, padx=5, pady=20)
            style.configure
            c = c + 1  # increase column by 1
            if c > 8:  # One line complete so change the row and column values
                r, c = r + 1, 0
    else:
        close_options()

    def my_upd():
        window.style.theme_use(my_str.get())
        style = boottk.Style()
        style.configure(button_style, font=(ffont, fsize))
        env.chenge_var("main_theme", my_str.get())

def tk_answer(output):
    try:
        answers.insert(tk.END, f"{output.decode(encoding='utf-8')}")
    except:
        print("")

def font_size_main(font_size):
    global answers
    global frame03
    global window
    os.environ["main_windows_font_size"] = str(font_size)
    env.chenge_var("main_windows_font_size", str(font_size))
    #reload text widget/frame with new font size
    remember_text = answers.get("1.0", boottk.END)
    answers.destroy()
    frame03.destroy()
    frame03 = boottk.Frame(window)
    frame03.grid(row = 0, column = 1, rowspan = 4)
    #size of text widget dipend on font size.
    #fix the change of size to the frame with this:
    #width=int(120-(4*int(font_size))),  height=int(70-(3.7*int(font_size))
    answers = boottk.Text(frame03, width=int(120-(4*int(font_size))),  height=int(74-(4.2*int(font_size))), font=(ffont, font_size))
    answers.grid(pady=20, padx=20, rowspan = 3)
    answers.insert("1.0", remember_text)

def save_showrun():
    ip_host = combo_box01.get().replace(".", "_")
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cmd_fix01 = date_time.replace(" ", "_")
    cmd_fix02 = cmd_fix01.replace(".", "_")
    cmd_fix03 = cmd_fix02.replace("/", "_")
    cmd_fix04 = cmd_fix03.replace(":", "_")
    new_file_name = f"{ip_host}_{cmd_fix04}.txt"

    filename = fd.asksaveasfilename(initialfile = new_file_name,
    defaultextension=".txt",filetypes=[("All Files","*.*"),("Text File","*.txt")])
    fix_filename = filename.replace("/", "\\")
    copy_command = f"copy script.txt {fix_filename}"
    if filename:
        os.system(copy_command)

def ai_the_script():
    with open(srun_file, "r") as file:
        sr_text = file.read()
        text = f"How can I improve this {combo_box02.get()} script\n{sr_text}"
        answer_ai = gem.ask_gemini(text)
        answers.delete("1.0", tk.END)
        answers.insert(tk.END, answer_ai)

def ask_gemini(answers09, entry09):
    user_input = entry09.get()
    entry09.delete(0, tk.END)
    if user_input != "":
        answer09_ai = gem.chat_gemini(user_input)
        random_color = random.choice(background_colors_list)
        answers09.tag_config(random_color, background=random_color, foreground="black")
        answers09.insert(tk.END, f"{answer09_ai}\n", random_color)
        answers09.see(tk.END)
    else:
        answers09.insert(tk.END, "Ask me anything :-)")

def ask_gemini_tread(answers09, entry09):
    thread03 = threading.Thread(target=ask_gemini(answers09, entry09))
    thread03.start()

def gemini_window(gemini_text):
    gemini_top = tk.Toplevel(window)
    gemini_top.title(f"Ask Gemini")
    size_position = os.getenv("gemini_size_position")
    gemini_top.geometry(size_position)
    gemini_top.protocol("WM_DELETE_WINDOW", (lambda : on_gemini_close(gemini_top, answers09)))
    gfont = os.getenv("gemini_font")
    gfont_size = os.getenv("gemini_font_size")

    menubar = tk.Menu(gemini_top)
    gemini_top.config(menu = menubar)
    settings_menu = tk.Menu(menubar)
    font_menu = tk.Menu(settings_menu, tearoff=0)
    size_menu = tk.Menu(settings_menu, tearoff=0)

    menubar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_cascade(label="Font", menu=font_menu, underline=0)
    with open("fonts.txt", "r") as file:
        fonts_list = file.readlines()
    for item in fonts_list:
        font_menu.add_command(label=item.rstrip(), command = lambda x = item.rstrip() : change_gfont(x, gemini_top, answers09))

    var_gfsize = tk.IntVar()
    settings_menu.add_cascade(label="Font Size", menu=size_menu, underline=0)
    for item in range(7,15):
        size_menu.add_radiobutton(label=str(item), value=item, variable=var_gfsize, command=lambda x=item:change_gsize(x, gemini_top, answers09), font=(main_font, main_fsize))
#    var_gfsize.set(14)

    settings_menu.add_command(label = "Load Default Settings", command = lambda: load_default_settings_gemini(gemini_top, answers09))

    answers09 = boottk.Text(gemini_top, wrap=WORD, width=65,  height=25, font=(gfont, gfont_size))
    answers09.pack(fill="both", expand=True)
    if gemini_text == "":
        answers09.insert(tk.END, "Hello, How can I help?\n:-)")
    else:
        answers09.insert("1.0", gemini_text)

    entry09 = boottk.Entry(gemini_top, justify='left', font=(ffont, fsize))
    entry09.pack(fill="both", expand=False)
    entry09.bind('<Return>', lambda x: ask_gemini_tread(answers09, entry09))

def on_gemini_close(gemini_top, answers09, default_position=False):
    size_position = gemini_top.winfo_geometry()
    #wait for final postion/last font/last size to save to env.
    #if False remember final postion
    #if True go back to default position
    if default_position == False:
        env.chenge_var("gemini_size_position", str(size_position))
    gemini_top.destroy()
    #clear chat history
    gem.on_chat_close()

def change_gfont(font_ch, gemini_top, answers09):
    os.environ["gemini_font"] = font_ch
    env.chenge_var("gemini_font", font_ch)
    reload_gemini(gemini_top, answers09)

def change_gsize(size_ch, gemini_top, answers09):
    os.environ["gemini_font_size"] = str(size_ch)
    env.chenge_var("gemini_font_size", str(size_ch))
    #for font/size change to be visble, reload the window
    reload_gemini(gemini_top, answers09, False)

def reload_gemini(gemini_top, answers09, default_position=False):
    #get the text from widget before destroy
    #so I can desplay it on reloaded window
    gemini_text = answers09.get("1.0", boottk.END)
    #close the top window, and open again with the new font/size values
    on_gemini_close(gemini_top, answers09, default_position)
    gemini_window(gemini_text)

def load_default_settings_gemini(gemini_top, answers09):
    #load from .env default values
    default_font = os.getenv("default_gemini_font")
    default_fsize = os.getenv("default_gemini_font_size")
    default_size_position = os.getenv("default_gemini_size_position")
    #set value into windows env
    os.environ["gemini_font"] = default_font
    #save values into .env file
    env.chenge_var("gemini_font", default_font)
    os.environ["gemini_font_size"] = default_fsize
    env.chenge_var("gemini_font_size", default_fsize)
    os.environ["gemini_size_position"] = default_size_position
    env.chenge_var("gemini_size_position", default_size_position)

    reload_gemini(gemini_top, answers09, True)

def chenge_response():
    radio_var = int(optionVar_radio.get())
    if radio_var == 1:
        response_time = "0.2"
    elif radio_var == 2:
        response_time = "0.5"
    elif radio_var == 3:
        response_time = "1"
    env.chenge_var("response_time", response_time)

def change_port():
    port_var = int(optionVar_port.get())
    if port_var == 1:
        port = "22"
    elif port_var == 2:
        port = "23"
    env.chenge_var("port", port)

#read previous host details and create a list. Need to be loaded first, for entry01-03
delete_host_duplicates()
read_host_file()

window = boottk.Window()
window.resizable(False,False)
my_theme = os.getenv("main_theme")
port = os.getenv("port")
fsize = os.getenv("main_windows_font_size")
window.style.theme_use(my_theme)
style = boottk.Style()
style.configure(button_style, font=(main_font, main_fsize))
window.title("Analize")
menubar = Menu(window)
window.config(menu = menubar)
settings_menu = Menu(menubar)
ask_gemini_menu = Menu(menubar)

menubar.add_cascade(label="Settings", menu=settings_menu, underline=0)
settings_menu.add_command(label = 'Choose Theme', command = lambda: change_theme(1), font=(main_font, main_fsize))
settings_menu.add_command(label = 'Clear Hosts List', command = clear_host_file, font=(main_font, main_fsize))

optionVar_fsize = StringVar()
font_size_menu = Menu(settings_menu, tearoff=0)
settings_menu.add_cascade(label='Font Size', menu=font_size_menu, underline=0)
for item in range(7,12):
    font_size_menu.add_radiobutton(label =str(item), value=item, variable=optionVar_fsize, command = lambda x=item:font_size_main(x), font=(main_font, main_fsize))
#    font_size_menu.add_command(label =str(item) , command = lambda x=item:font_size_main(x), font=(ffont, fsize))
optionVar_fsize.set(fsize)

optionVar_radio = StringVar()
response_menu = Menu(settings_menu, tearoff=0)
response_menu.add_radiobutton(label="Fast - 0.2Sec", value=1, variable=optionVar_radio, command=chenge_response)
response_menu.add_radiobutton(label="Medium - 0.5Sec", value=2, variable=optionVar_radio, command=chenge_response)
response_menu.add_radiobutton(label="Slow - 1Sec", value=3, variable=optionVar_radio, command=chenge_response)
settings_menu.add_cascade(label="Response Time", menu=response_menu)
if response_time == 0.2:
    optionVar_radio.set(1)
elif response_time == 0.5:
    optionVar_radio.set(2)
elif response_time == 1:
    optionVar_radio.set(3)

#optionVar_port = StringVar()
#port_radio = Menu(settings_menu, tearoff=0)
#port_radio.add_radiobutton(label="SSH - Port 22", value=1, variable=optionVar_port, command=change_port)
#port_radio.add_radiobutton(label="Telnet - Port 23", value=2, variable=optionVar_port, command=change_port)
#settings_menu.add_cascade(label="SSH/Telnet", menu=port_radio)
#if port == "22":
#    optionVar_port.set(1)
#elif port == "23":
#    optionVar_port.set(2)


menubar.add_cascade(label="Ask Gemini", menu=ask_gemini_menu, underline=0)
ask_gemini_menu.add_command(label ="Ask Gemini" , command = lambda: gemini_window(""))

frame01 = boottk.Frame(window)
frame01.grid(row = 1, column = 0, sticky="ne")
frame05 = boottk.Frame(window)
frame05.grid(row = 2, column = 0, sticky="ne")
frame02 = boottk.Frame(window)
frame02.grid(row = 3, column = 0, sticky="ne")
frame03 = boottk.Frame(window)
frame03.grid(row = 1, column = 1, rowspan = 4)

label00 = boottk.Label(frame01, text = "Connect SSH:", font=(ffont, str(int(main_fsize)+1), "bold"))
label00.grid(row = 0, column =0, pady = lpady, sticky="ne")

label01 = boottk.Label(frame01, text = " Host IP", font=(main_font, main_fsize, "bold"))
label01.grid(row = 1, column =0, sticky=NW)
combo_box01 = ttk.Combobox(frame01, width=entry_width-2, values="enter ip here", font=(main_font, main_fsize))
combo_box01['values'] = host_list
combo_box01.bind('<<ComboboxSelected>>', check_input)
combo_box01.grid(row = 1, column =1, sticky=NW)
if len(host_list) > 0:
    combo_box01.current(0)

label04 = boottk.Label(frame01, text = " OS", font=(main_font, main_fsize, "bold"))
label04.grid(row = 2, column =0, sticky=NW)
combo_box02 = ttk.Combobox(frame01, width=entry_width-2, font=(main_font, main_fsize))
combo_box02['values'] = ["Cisco", "Juniper"]
combo_box02.grid(row = 2, column =1, sticky=NW)

label02 = boottk.Label(frame01, text = " Username  ", font=(main_font, main_fsize, "bold"))
label02.grid(row = 3, column =0, sticky=NW)
entry02 = boottk.Entry(frame01, width = entry_width, justify='left', font=(main_font, main_fsize))
entry02.grid(row = 3, column = 1, sticky=NW)
if len(host_detail_list) > 0:
    entry02.insert(0, host_detail_list[0][1])

label03 = boottk.Label(frame01, text = " Password  ", font=(main_font, main_fsize, "bold"), justify='left')
label03.grid(row = 4, column =0, pady = lpady, sticky=NW)
entry03 = boottk.Entry(frame01, width = entry_width, justify='left', show="***", font=(main_font, main_fsize))
entry03.grid(row = 4, column = 1, sticky=NW)
if len(host_detail_list) > 0:
    entry03.insert(0, new_list[0][2])

#set defualt value 'ON' to checkbox
checkbutton01_var = IntVar(value=1)
checkbox01 = boottk.Checkbutton(frame01, text = "Remember Me", variable = checkbutton01_var, onvalue = 1, offvalue = 0)
checkbox01.grid(row = 5, column = 0, columnspan = 2, sticky=NW)

button01 = boottk.Button(frame05, text = "Analize", width = b_width, style=button_style, command= analize_run)
button01.grid(row = 2, column = 0, pady=5)
button02 = boottk.Button(frame05, text = "Open Terminal", width = b_width, style=button_style, command= lambda: terminal("Hello :)\n"))
button02.grid(row = 1, column = 0, pady=5)
button03 = boottk.Button(frame05, text = "Ping Host", width = b_width, style=button_style, command= check_ping_tread)
button03.grid(row = 3, column = 0, pady=5)

button11 = boottk.Button(frame02, text = "Interfaces", width = b_width, style=button_style, command= lambda: show_ana(1))
button11.grid(row = 0, column = 0, pady=2, padx=5)
button11.configure(state="disable")
button12 = boottk.Button(frame02, text = "Routes", width = b_width, style=button_style, command= lambda: show_ana(2))
button12.grid(row = 1, column = 0, pady=5)
button12.configure(state="disable")
button13 = boottk.Button(frame02, text = "Arp", width = b_width, style=button_style, command= lambda: show_ana(3))
button13.grid(row = 2, column = 0, pady=5)
button13.configure(state="disable")
button14 = boottk.Button(frame02, text = "Vrf", width = b_width, style=button_style, command= lambda: show_ana(7))
button14.grid(row = 3, column = 0, pady=5)
button14.configure(state="disable")
button15 = boottk.Button(frame02, text = "Routes Conf.", width = b_width, style=button_style, command= lambda: show_ana(4))
button15.grid(row = 4, column = 0, pady=5)
button15.configure(state="disable")
button16 = boottk.Button(frame02, text = "Interfaces Conf.", width = b_width, style=button_style, command= lambda: show_ana(6))
button16.grid(row = 5, column = 0, pady=5)
button16.configure(state="disable")
button17 = boottk.Button(frame02, text = "Version & Up Time", width = b_width, style=button_style, command= lambda: show_ana(5))
button17.grid(row = 6, column = 0, pady=5)
button17.configure(state="disable")
button18 = boottk.Button(frame02, text = "Gemini the Configuration", width = b_width, style=button_style, command = ai_the_script)
button18.grid(row = 7, column = 0, pady=5)
button18.configure(state="disable")
button19 = boottk.Button(frame02, text = "Save All Scripts", width = b_width, style=button_style, command = save_showrun)
button19.grid(row = 8, column = 0, pady=5)
button19.configure(state="disable")

answers = boottk.Text(frame03, wrap=WORD, width=int(120-(4*int(fsize))), height=int(74-(4.2*int(fsize))), font=(ffont, fsize))
answers.grid(pady=20, padx=20, rowspan = 3)

window.protocol("WM_DELETE_WINDOW", lambda : on_app_close())
window.mainloop()
