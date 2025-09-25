#!/usr/bin/env python

import subprocess
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change mac address")
    parser.add_option("-a", "--address", dest="address", help="New mac address")
    return parser.parse_args()

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

(options,args) = get_arguments()
change_mac(options.interface,options.address)

