import re
import time
import requests
from multiprocessing import Process

filename = "script.txt"
domain_file = "domain.txt"
adgroups_file = "ad_groups.txt"
adusers_file = "ad_users.txt"

afiles_list = [domain_file, adgroups_file, adusers_file]

def domain(lines):
    counter = 0
    to_print = "\n"
    for line in lines:
        find_start = re.search("powershell systeminfo", line)
        counter +=1
        if find_start:
            line_sinterface = counter
            break
    for line in lines[counter:]:
        find_end = re.search("#", line)
        if find_end:
            break
        elif line != "\n":
            to_print += f"{line}\n"
    to_print_fun(to_print, domain_file)

def ad_groups(lines):
    pass

def ad_users(lines):
    to_find = "powershell.exe Get-ADUser"
    counter = 0
    to_print = " AD Users\n"
    for line in lines:
        find_start = re.search(to_find, line)
        counter +=1
        if find_start:
            print("start")
            line_sinterface = counter
            break
    for line in lines[counter:]:
        find_mark01 = re.search("DistinguishedName", line)
        find_end = re.search("#", line)
        if find_end:
            break
        elif find_mark01:
            sline = line.split(":")
            split2 = sline[1].split(",")
            to_print += f"User: {split2[0][4:]}, Group: {split2[1][3:]}, Domain:{split2[2][3:]}.{split2[3][3:]}\n"
    to_print_fun(to_print, adusers_file)

def to_print_fun(to_print = "", to_file=""):
    with open(to_file, "a") as file:
        file.write(to_print)

def run_it():
    #clean previous analize files
    for item in afiles_list:
        with open(item, "w") as afile:
            afile.write("")
    with open(filename, "r") as file:
        lines = file.readlines()
    domain(lines)
    ad_groups(lines)
    ad_users(lines)
