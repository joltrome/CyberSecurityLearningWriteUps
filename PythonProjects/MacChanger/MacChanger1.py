#!/usr/bin/env python

import subprocess
import optparse

parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change mac address")
parser.add_option("-a", "--address", dest="address", help="New mac address")
(options, arguments) = parser.parse_args()

interface = options.interface
new_mac= options.address

print("[+] Changing MAC Address for " + interface + " to " + new_mac)

# subprocess.call("ifconfig " +  interface + " down", shell=True)
# subprocess.call("ifconfig " +  interface + " hw ether " +  new_mac , shell=True)
# subprocess.call("ifconfig " +  interface + " up", shell=True)
# subprocess.call("ifconfig", shell=True)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])
subprocess.call(["ifconfig"])
