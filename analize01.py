import re
import time
import requests
from multiprocessing import Process

filename = "script.txt"
analisys_file = "analisys.txt"
version_file = "version.txt"
interfaces_file = "interface.txt"
routes_file = "routes.txt"
arp_file = "arp.txt"
dinamic_file = "dinamic.txt"
interface_conf_file = "interface_conf_file.txt"
vrf_file = "vrf.txt"
summary_file = "summary.txt"
afiles_list = [analisys_file, version_file, interfaces_file, routes_file, arp_file, dinamic_file, interface_conf_file, vrf_file, summary_file]
sinterface = "show ip inter br"
sroute_static = "show ip route stat"
sroute_bgp = "show ip route bgp"
sroute_eigrp = "show ip route eigrp"
sarp = "show ip arp"
stime = "show time"
srun = "show run"
sversion = "show version"
suptime = "uptime is"
router_mark = "Router#"
interface_mark = "Interface"
eigrp_srun = "router eigrp"
bgp_srun = "router bgp"
svrf = "show ip vrf"
up_mark = "up"
down_mark = "down"
arpa_mark = "ARPA"
static_mark = "S*"
bgp_mark = "B"
ospf_mark = "O"
eigrp_mark = "D"
stop_mark = "!"
unassigned_mark = "unassigned"
line_sinterface = 0
arp_ip_list = []

interfaces_ips = {"iterface" : "ip"}
interfaces_macs = {"interface" : "arp"}


def analize_interafes(lines):
    line_sinterface = 0
    to_print = "Intarfaces:\n"
#    with open(interfaces_file, "w") as interfile:
#        interfile.write("Intarfaces:\n")
    counter = 0
    for line in lines:
        find_end = re.search(sinterface, line)
        counter +=1
        if find_end:
            line_sinterface = counter
            break

    for line in lines[line_sinterface:]:
        find_end = re.search(".#", line)
        if find_end:
            break
        elif line != "\n":
            items = (line.split())
            if up_mark in items:
                to_print += f"UP, {line}\n"
                interfaces_ips[items[0]] = items[1]

            elif down_mark in items:
                to_print += f"DOWN {line}\n"

                interfaces_ips[items[0]] = items[1]
    to_print_fun(to_print, interfaces_file)

def analyze_arp(lines):
    global arp_ip_list
    to_print = "Show Arp Results\n"
    counter = 0
    for line in lines:
        counter +=1
        if sarp in line:
            line_sarp = counter
            break
    for line in lines[line_sarp:]:
        find_end = re.search(".#", line)
        if find_end:
            break
        elif line != "\n":
            items = (line.split())
            if arpa_mark in items:
                list_len = len(items)
                if list_len > 5:
                    mac_vendure = mac_lookup(items[3])
                    to_print += f'{items[5]} | {items[1]} | {items[3]} | {mac_vendure}\n\n'
                    interfaces_macs[items[1]] = items[3]
                else:
                    mac_vendure = mac_lookup(items[3])
                    to_print += f'{items[1]} | {items[3]} | {mac_vendure}\n\n'
                    interfaces_macs[items[1]] = items[3]

    to_print_fun(to_print, arp_file)

def route_analyze_static(lines):
    to_print = "Route Table\n Static:\n"
    counter = 0
    static_ex = False
    line_number_sroute = 0
    for line in lines:
        counter +=1
        find_static = re.search("show ip route stat", line)
        if find_static:
            line_number_sroute = counter
            break

    for line01 in lines[line_number_sroute:]:
        find_end = re.search("^#", line01)
        if find_end:
          break
        elif line01 != "\n":
            find_static01 = re.search(r"^S", line01)
            find_static02 = re.search(r"^[S*]", line01)
            if "Code" in line01:
                continue
            elif find_static01 or find_static02:
                to_print += line01
                static_ex = True
    if static_ex is False:
        to_print += "No Static Routes Found"

    to_print_fun(to_print, routes_file)


def route_analyze_bgp(lines):
    with open(routes_file, "a") as rbfile:
        rbfile.write("BGP:\n")
    to_print = f"BGP Routes:\n"
    to_print_fun(to_print, analisys_file)
    counter = 0
    bgp_ex = False

    for line in lines:
        counter +=1
        find_bgp = re.search("show ip route bgp", line)
        if find_bgp:
            line_number_sbgp = counter
            break

    for line in lines[line_number_sbgp:]:
        find_end = re.search("^#", line)
        if find_end:
          break
        elif line != "\n":
            find_static = x = re.search("^B", line)
            if find_static:
                to_print += line
                bgp_ex = True
    if bgp_ex is False:
        to_print += "No BGP Routes\n"

    to_print_fun(to_print, routes_file)

def route_analyze_eigrp(lines):
    with open(routes_file, "a") as refile:
        refile.write("EIGRP:\n")
    to_print_fun("", analisys_file)
    counter = 0
    eigrp_ex = False
    to_print = ""
    for line in lines:
        counter +=1
        find_bgp = re.search("show ip route eigrp", line)
        if find_bgp:
            line_number_seigrp = counter
            break

    for line in lines[line_number_seigrp:]:
        find_end = re.search("^#", line)
        if find_end:
          break
        elif line != "\n":
            find_static = x = re.search("^D", line)
            if find_static:
                to_print += line
                eigrp_ex = True
    if eigrp_ex is False:
        to_print += "No EIGRP Routes\n"

    to_print_fun(to_print, routes_file)


def analize_srun(lines):
    to_print = "Intarfaces Configurarions\n"
    counter = 0
    for line in lines:
        counter +=1
        if srun in line:
            line_number_srun = counter
            break

    for line in lines[line_number_srun:]:
        line_number_srun +=1
        find_end = re.search(".#", line)
        if find_end:
            break
        elif line != "\n":
            items = (line.split())
            for dic_item, dic_value in interfaces_ips.items():
                find_item = re.search(f"interface {dic_item}", line)
                if find_item:
                    for srun_line in lines[line_number_srun-2:]:
                        find_end = re.search(stop_mark, srun_line)
                        if find_end:
                            to_print += "---------------\n"
                            break
                        elif srun_line != "\n":
                            to_print += srun_line
    to_print_fun(to_print, interface_conf_file)

def srun_dinamic_routes(lines):
    to_print = "Dianamic Routes Configuration\n"
    counter = 0
    for line in lines:
        counter +=1
        if srun in line:
            line_number_srun = counter
            break

    for line in lines[line_number_srun:]:
        line_number_srun +=1
        find_end = re.search(".#", line)
        if find_end:
            break
        elif line != "\n":
            items = (line.split())
            if bgp_srun in line:
                to_print_bgp = "\nBGP Configuration\n------------------\n"
                to_print_fun(to_print_bgp, analisys_file)
                for srun_line in lines[line_number_srun-2:]:
                    find_end = re.search("^!", srun_line)
                    if find_end:
                        to_print += "---------------\n"
                        break
                    elif srun_line != "\n":
                        to_print += srun_line

            if eigrp_srun in line:
                to_print_eigrp = "\nEIGRP Configuration\n------------------\n"
                to_print_fun(to_print_eigrp, analisys_file)
                for srun_line in lines[line_number_srun-2:]:
                    find_end = re.search("^!", srun_line)
                    if find_end:
                        to_print += "---------------\n"
                        break
                    elif srun_line != "\n":
                        to_print += srun_line
    to_print_fun(to_print, dinamic_file)

def sversion_sec(lines):
    counter = 0
    ver_counter = 0
    to_print = "Machine Version/Up Time\n"
    for line in lines:
        counter +=1
        find_ver_start = re.search(sversion, line)
        if find_ver_start:
            line_number_srun = counter
            break

    for line in lines[line_number_srun:]:
        ver_counter +=1
        find_end = re.search(".#", line)
        find_ver = re.search("Version", line)
        if find_end:
            break
        elif line != "\n" and find_ver:
            to_print += f"\n{line}\n"
        elif suptime in line:
            to_print += f"Router UP Time: {line}\n\n"

    to_print_fun(to_print, version_file)

def ana_vrf(lines):
    to_print = "Vrf's\n"
    counter = 0
    for line in lines:
        counter +=1
        if svrf in line:
            line_number = counter
            break

    for line in lines[line_number:]:
        find_end = re.search(".#", line)
        if find_end:
            break
        elif line != "\n":
            to_print += line
    to_print_fun(to_print, vrf_file)

def summary(lines):
    pass

def mac_lookup(mac_address):
    try:
        url = f'https://www.macvendorlookup.com/api/v2/{mac_address}'
        vendor = requests.get(url).json()
        time.sleep(1)
        vendor_text = vendor[0]['company']
        return vendor_text
    except:
        vendor_text = "UnNone"
        return vendor_text

def to_print_fun(to_print = "", to_file=""):
    with open(analisys_file, "a") as file:
        file.write(to_print)
    with open(to_file, "a") as file:
        file.write(to_print)

def run_it():
    #clean previous analize files
    for item in afiles_list:
        with open(item, "w") as afile:
            afile.write("")
    with open(filename, "r") as file:
        lines = file.readlines()
    sversion_sec(lines)
    analize_interafes(lines)
    route_analyze_static(lines)
    route_analyze_bgp(lines)
    route_analyze_eigrp(lines)
    srun_dinamic_routes(lines)
    analyze_arp(lines)
    analize_srun(lines)
    ana_vrf(lines)
