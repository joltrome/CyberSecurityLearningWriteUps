#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change mac address")
    parser.add_option("-a", "--address", dest="address", help="New mac address")
    (options,args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.address:
        parser.error("[-] Please specify an address, use --help for more info")
    return options

def change_mac(interface,new_mac_address):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac_address)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_interface = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_interface)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] No MAC Address Found")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC Address: " + str(current_mac))
change_mac(options.interface,options.address)
current_mac = get_current_mac(options.interface)
if current_mac == options.address:
    print("[+] MAC Address Changed Successfully to " + options.address)
else:
    print("[-] MAC Address did not get changed")
