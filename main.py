#!/usr/bin/python3
#-*- coding: utf-8 -*-

from wifi import *
import matplotlib.pyplot as plt

ip = '192.168.22.21'
port = 22
username = 'root'
password = 'password'

def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    device = reomte_device(ip, port, username, password)
    device.scanning()
    aps = []
    fre2_4 = []
    fre5 = []
    ssid = []
    level = []

    for msg in device.message:
        aps.append(dumpAp(msg))

    plt.figure(12)
    plt.subplot(221)
    plt.xticks(rotation=-30)
    for dev in aps:
        print(dev.ssid)
        print(dev.freq)
        print(dev.level)
        if dev.freq > 5:
            fre5.append(dev)
        else:
            fre2_4.append(dev)

    for f2_4 in fre2_4:
        ssid.append(f2_4.ssid)
        level.append(f2_4.level)
        plt.bar(ssid, level)
        plt.title('2.4G')

    
    plt.subplot(222)
    ssid5G = []
    level5G = []

    for f5 in fre5:
        ssid5G.append(f5.ssid)
        level5G.append(f5.level)
        plt.bar(ssid5G, level5G)
        plt.title('5G')
    plt.draw() 
    plt.pause(0.5)

if __name__ == '__main__':
    while True:
        main()