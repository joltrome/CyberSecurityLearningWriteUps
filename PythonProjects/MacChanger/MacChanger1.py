#!/usr/bin/env python

import subprocess
import optparse

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

    # subprocess.call("ifconfig " +  interface + " down", shell=True)
    # subprocess.call("ifconfig " +  interface + " hw ether " +  new_mac , shell=True)
    # subprocess.call("ifconfig " +  interface + " up", shell=True)
    # subprocess.call("ifconfig", shell=True)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig"])

options = get_arguments()
change_mac(options.interface,options.address)

