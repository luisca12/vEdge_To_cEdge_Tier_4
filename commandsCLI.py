from netmiko import ConnectHandler
from log import authLog

import traceback
import ipaddress
import re
import os

shInt1101 = "show run interface vlan 1105 | inc ip address"
shInt1103 = "show run interface vlan 1107 | inc ip address"
shVlanMgmt = "show run interface vlan 1500 | inc ip address"
shLoop0 = "show run interface lo0 | inc ip address"

shIntDesSDW = "show interface description | inc SDW|sdw"
shIntDesCON = "show interface description | inc CON"

intPatt = r'[a-zA-Z]+\d+\/(?:\d+\/)*\d+'

def shCoreInfo(swHostname, username, netDevice):

    try:
        currentNetDevice = {
            'device_type': 'cisco_xe',
            'ip': swHostname,
            'username': username,
            'password': netDevice['password'],
            'secret': netDevice['secret'],
            'global_delay_factor': 2.0,
            'timeout': 120,
            'session_log': 'netmikoLog.txt',
            'verbose': True,
            'session_log_file_mode': 'append'
        }

        print(f"Connecting to device {swHostname}...")
        with ConnectHandler(**currentNetDevice) as sshAccess:
            try:
                sshAccess.enable()
                authLog.info(f"Generating hostname for {swHostname}")
                shHostnameOut = re.sub(".mgmt.internal.das|.cm.mgmt.internal.das|.mgmt.wellpoint.com","#", swHostname)
                authLog.info(f"Hostname for {swHostname}: {shHostnameOut}")
                print(f"INFO: This is the hostname: {shHostnameOut}")

                shInt1101Out = sshAccess.send_command(shInt1101)
                authLog.info(f"Automation successfully ran the command \"{shInt1101}\" on device {swHostname}\n{shHostnameOut}{shInt1101}\n{shInt1101Out}")
                ipVlan1101 = shInt1101Out.split(' ')[3]
                print(f"INFO: Found the following IP for Vlan1101: {ipVlan1101}")
                authLog.info(f"Found the following IP for Vlan1101:{ipVlan1101}")
                maskVlan1101 = shInt1101Out.split(' ')[4]
                print(f"INFO: Found the following Mask for Vlan1101: {maskVlan1101}\n")
                authLog.info(f"Found the following Mask for Vlan1101:{maskVlan1101}")
                netVlan1101 = ipaddress.IPv4Network(f"{ipVlan1101}/{maskVlan1101}", strict=False).network_address
                authLog.info(f"Found the network for Vlan1101:{netVlan1101}")

                shInt1103Out = sshAccess.send_command(shInt1103)
                authLog.info(f"Automation successfully ran the command \"{shInt1103}\" on device {swHostname}\n{shHostnameOut}{shInt1103}\n{shInt1103Out}")
                ipVlan1103 = shInt1103Out.split(' ')[3]
                print(f"INFO: Found the following IP for Vlan1103: {ipVlan1103}")
                authLog.info(f"Found the following IP for Vlan1103:{ipVlan1103}")
                maskVlan1103 = shInt1103Out.split(' ')[4]
                print(f"INFO: Found the following Mask for Vlan11033: {maskVlan1103}\n")
                authLog.info(f"Found the following Mask for Vlan1103:{maskVlan1103}")
                netVlan1103 = ipaddress.IPv4Network(f"{ipVlan1103}/{maskVlan1103}", strict=False).network_address
                authLog.info(f"Found the network for Vlan1103:{netVlan1103}")

                shIntDesSDWOut = sshAccess.send_command(shIntDesSDW)
                print(f"INFO: This is {shIntDesSDW}:\n{shIntDesSDWOut}\n")
                authLog.info(f"Automation successfully ran the command \"{shIntDesSDW}\" on device {swHostname}\n{shHostnameOut}{shIntDesSDW}\n{shIntDesSDWOut}")

                shIntDesCONOut = sshAccess.send_command(shIntDesCON)
                shIntDesCONOut1 = re.findall(intPatt, shIntDesCONOut)
                print(f"INFO: Show int Des | inc Con:\n{shIntDesCONOut}\nInterfaces:{shIntDesCONOut1}\n")
                authLog.info(f"Automation successfully ran the command \"{shIntDesCON}\" on device {swHostname}\n{shHostnameOut}{shIntDesCON}\n{shIntDesCONOut}")
                authLog.info(f"Automation successfully found the following interfaces: {shIntDesCONOut1}")

                shVlanMgmtOut = sshAccess.send_command(shVlanMgmt)
                authLog.info(f"Automation successfully ran the command \"{shVlanMgmt}\" on device {swHostname}\n{shHostnameOut}{shVlanMgmt}\n{shVlanMgmtOut}")
                shVlanMgmtIP = shVlanMgmtOut.split(' ')[3]
                print(f"INFO: Found the Management VLAN (1500) IP: {shVlanMgmtIP}")
                authLog.info(f"Found the Management VLAN (1500) IP:{shVlanMgmtIP}")
                shVlanMgmtMask = shVlanMgmtOut.split(' ')[4]
                print(f"INFO: Found the Management VLAN (1500) Mask: {shVlanMgmtMask}")
                authLog.info(f"Found the Management VLAN (1500) Mask: {shVlanMgmtMask}")
                shVlanMgmtCIDR = ipaddress.IPv4Network(f'{shVlanMgmtIP}/{shVlanMgmtMask}', strict=False).prefixlen
                print(f"INFO: Found the Management VLAN (1500) CIDR: {shVlanMgmtCIDR}\n")
                authLog.info(f"Found the Management VLAN (1500) CIDR: {shVlanMgmtCIDR}")

                shLoop0Out = sshAccess.send_command(shLoop0)
                authLog.info(f"Automation successfully ran the command \"{shLoop0}\" on device {swHostname}\n{shHostnameOut}{shLoop0}\n{shLoop0Out}")
                shLoop0Out = shLoop0Out.split(' ')[3]
                print(f"INFO: Found the Switch Loopback 0 IP: {shLoop0Out}\n")
                authLog.info(f"Found the Switch Loopback 0 IP: {shVlanMgmtCIDR}")

                os.system("PAUSE")

                return shHostnameOut, netVlan1101, netVlan1103, shIntDesSDWOut, shIntDesCONOut1, shVlanMgmtIP, shVlanMgmtCIDR, shLoop0Out

            except Exception as error:
                print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
                authLog.error(f"User {username} connected to {swHostname} got an error: {error}")
                authLog.debug(traceback.format_exc(),"\n")
    
    except Exception as error:
        print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
        authLog.error(f"User {username} connected to {swHostname} got an error: {error}")
        authLog.debug(traceback.format_exc(),"\n")
        with open(f"failedDevices.txt","a") as failedDevices:
            failedDevices.write(f"User {username} connected to {swHostname} got an error.\n")