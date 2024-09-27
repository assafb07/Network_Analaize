import re
import time
import requests

filename = "script.txt"
analisys_file = "analisys.txt"
version_file = "version.txt"
interfaces_file = "interface.txt"
routes_file = "routes.txt"
arp_file = "arp.txt"
dinamic_file = "dinamic.txt"
interface_conf_file = "interface_conf_file.txt"
vrf_file = "vrf.txt"
srun  = "show configuration | display set | no-more"
sinterface = "show configuration interfaces | display set | no-more"
svrf = "show configuration routing-instance"
stop_mark = "^#"
afiles_list = [analisys_file, version_file, interfaces_file, routes_file, arp_file, dinamic_file, interface_conf_file, vrf_file]


def analize_interafes(sfile):
    counter = 0
    interface_line = 0
    with open(interfaces_file, "w") as interfile:
        interfile.write("Intarfaces:\n\n")
    for line in sfile:
        counter +=1
        if "show interfaces terse" in line:
            interface_line = counter
            break
    for line in sfile[interface_line:]:
        find_end = re.search("^#", line)
        if find_end:
            break
        elif line != "\n":
            sline = line.split()
            if len(sline) > 4:
                to_print = f"{line}\n"
                to_print_fun(to_print, interfaces_file)

def analyze_arp(sfile):
    counter = 0
    arp_line = 0
    line_counter = 0
    with open(arp_file, "w") as apile:
        apile.write("Arp Table:\n\n")
    for line in sfile:
        counter +=1
        if "show arp no-resolve" in line:
            arp_line = counter
            break
    for line in sfile[arp_line:]:
        find_end = re.search("^#", line)
        if find_end:
            break
        elif line != "\n":
            line_list = line.split()
            if len(line_list) > 3 and line_counter>1:
                mac_vendure = mac_lookup(line_list[0])
                to_print = f"{line_list[2]} | {line_list[1]} | {line_list[0]}| vendor:{mac_vendure}\n\n"
                to_print_fun(to_print, arp_file)
        line_counter+=1


def route_analyze(lines):
    to_print = "Route Table\n\n"
    counter = 0
    line_number_sroute = 0

    for line in lines:
        counter +=1
        find_static = re.search("show route table", line)
        if find_static:
            line_number_sroute = counter
            break

    for line01 in lines[line_number_sroute:]:
        find_end = re.search("^#", line01)
        if find_end:
          break
        elif line01 != "\n":
             to_print += line01

    to_print_fun(to_print[:-7], routes_file)

def analize_configuration(lines):
    to_print = "Intarfaces Configurarions\n"
    counter = 0
    for line in lines:
        counter +=1
        if sinterface in line:
            line_number_srun = counter
            break

    for srun_line in lines[line_number_srun:]:
        find_end = re.search(stop_mark, srun_line)
#        find_item = re.search("set interfaces", srun_line)
        if find_end:
            break
        else:
            to_print += srun_line
    to_print_fun(to_print[:-7], interface_conf_file)


def sversion_sec(lines):
    to_print = "Verion\n\n"
    counter = 0
    couter01 = 0
    line_number_sroute = 0

    for line in lines:
        counter +=1
        find_static = re.search("show version", line)
        if find_static:
            line_number_ver = counter
            break

    for line01 in lines[line_number_ver:]:
        find_end = re.search(".#", line01)
        if find_end:
          break
        elif line01 != "\n" and couter01 < 4:
            couter01+=1
            to_print += line01
    to_print_fun(to_print, version_file)

def sup_time(lines):
    to_print = "Up Time:\n\n"
    counter = 0

    for line in lines:
        counter +=1
        find_static = re.search("show system uptime ", line)
        if find_static:
            line_number_ver = counter

    for line01 in lines[line_number_ver:]:
        find_end = re.search("^#", line01)
        if find_end:
          break
        elif line01 != "\n":
            to_print += line01
    to_print_fun(to_print[:-7], version_file)

def route_conf(lines):
    to_print = "Routing Configurarions\n"
    counter = 0

    for line in lines:
        counter +=1
        pattern = r'\b' + re.escape(srun) + r'\b'
        find_item = re.search(pattern, line)
        if find_item:
            line_number_srun = counter
            break

    for srun_line in lines[line_number_srun:]:
        find_end = re.search(stop_mark, srun_line)
        find_item01 = re.search(r"static", srun_line)
        find_item02 = re.search(r"bgp", srun_line)
        find_item03 = re.search(r"eigrp", srun_line)
        find_item04 = re.search(r"rip", srun_line)
        if find_end:
            break
        elif find_item01 or find_item02 or find_item03 or find_item04:
            to_print += srun_line
    to_print_fun(to_print, dinamic_file)

def ana_vrf(lines):
    to_print = "VRF / Routing Instance:\n\n"
    counter = 0
    for line in lines:
        counter +=1
        find_vrf = re.search(svrf, line)
        if find_vrf:
            line_number_vrf = counter
            break

    for line01 in lines[line_number_vrf:]:
        find_end = re.search("^#", line01)
        if find_end:
          break
        elif line01 != "\n":
            to_print += line01
    to_print_fun(to_print[:-7], vrf_file)


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
    for item in afiles_list:
        with open(item, "w") as afile:
            afile.write("")
    with open(filename, "r") as file:
        lines = file.readlines()
    analize_interafes(lines)
    analyze_arp(lines)
    route_analyze(lines)
    analize_configuration(lines)
    sversion_sec(lines)
    sup_time(lines)
    route_conf(lines)
    ana_vrf(lines)
