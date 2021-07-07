#!/usr/bin/python3
#-*- coding: utf-8 -*-
import paramiko
import re

class ap:
    
    def __init__(self, ssid, level, freq):
        self.ssid = ssid
        self.level = level
        self.freq = freq

class reomte_device:

    def __init__(self, ip, port, username, password):
        self.ipaddress = ip
        self.port = port
        self.username = username
        self.password = password

        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ipaddress, self.port, self.username, self.password, timeout=5)
            print('connected %s\n'%(self.ipaddress))

        except:
            print('connect %s error!\n'%(self.ipaddress))

    def scanning(self):
        stdin,stdout,stderr = self.ssh.exec_command('iwlist wlan0 scanning')
        message = [[]]
        counter = 0

        for line in stdout.readlines():
            searchObj = re.search('Cell', line)
            if searchObj:
                message.append([])
                counter += 1

            message[counter].append(line)
            
        self.message = message[1:]

def findMessage(str, target, find_start, find_end):
    searchObj = re.search(target, str)
    start = 0
    end = 0
    if searchObj:
        start = str.find(find_start) + 1
        end = start + str[start + 1:].find(find_end) + 1
    return searchObj,start,end

def dumpAp(message):
    ssid = ''
    freq = 0.0
    level = 0

    for line in message:
        searchObj,start,end = findMessage(line, 'ESSID', '"', '"')
        if searchObj:
            ssid = line[start:end]
        
        searchObj,start,end = findMessage(line, 'Frequency', ':', ' GHz')
        if searchObj:
            freq = float(line[start:end])

        searchObj,start,end = findMessage(line, 'Signal level', 'level=', ' dBm')
        if searchObj:
            level = int(line[start + 5:end])
        
    return ap(ssid, level, freq)
        

if __name__ == '__main__':
    device = reomte_device('192.168.22.63', 22, 'root', 'password')
    device.scanning()
    aps = []
    for msg in device.message:
        aps.append(dumpAp(msg))

    for dev in aps:
        print(dev.ssid)
        print(dev.freq)
        print(dev.level)