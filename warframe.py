'''
Author       : Primimy
Date         : 2022-07-27 00:12:51
This script aims to automatically login in warframe and get daily bonus.
'''

import os
import subprocess
import time

import python_hosts
import pywinauto.mouse
import tqdm
from pywinauto.application import Application

warframePath = "C:/Users/primi/Desktop/Warframe.url"
warframeLauncherWaitTime = 1500
bounsCoords1, bounsCoords2 = (937, 572), (935, 683)


def isProcessRunning(processName):
    return (str(subprocess.check_output("powershell.exe -Command \"ps | Where-Object ProcessName -eq " + processName + " \"", shell=True)).find(processName) != -1)


print("Kill process Launcher.exe Warframe.x64.exe")
os.popen(r'sudo taskkill /f /im Launcher.exe')
os.popen(r'sudo taskkill /f /im Warframe.x64.exe')
if (isProcessRunning("steam")):
    warframeLauncherWaitTime = 300

print("Write update hosts")
hosts = python_hosts.Hosts(path="C:/Windows/System32/drivers/etc/hosts")
hosts.remove_all_matching(name='content.warframe.com')
hosts.remove_all_matching(address='23.67.163.105')
# hosts.add([python_hosts.HostsEntry(entry_type='ipv4',address='151.139.33.35', names=['content.warframe.com'])])
hosts.write()

print("Starting Warframe Launcher")
os.popen(warframePath)
for i in tqdm.trange(warframeLauncherWaitTime):
    time.sleep(0.01)

try:
    app = Application().connect(title="Steam 对话")
    app['Steam 对话'].click_input(button='left', coords=(170, 219))
    print("skip steam save data and run game\nConnect Launcher")
except:
    print("Connect Launcher")

while True:
    if not isProcessRunning("Launcher"):
        time.sleep(1)
    else:
        break

time.sleep(1)
app = Application().connect(title="Warframe")
app['Warframe'].wait('visible')

print("Waiting for update")
for i in range(0, 1000):
    if (not isProcessRunning("Launcher")) and (isProcessRunning("Warframe.x64")):
        break
    else:
        try:
            app['Warframe'].click_input(button='left', coords=(724, 595))
        except:
            pass
        time.sleep(1)

print("remove update hosts and write login hosts")
hosts.remove_all_matching(name='content.warframe.com')
# hosts.add([python_hosts.HostsEntry(entry_type='ipv4',address='23.67.163.105',names=['origin.warframe.com'])])
# hosts.add([python_hosts.HostsEntry(entry_type='ipv4',address='23.67.163.105',names=['api.warframe.com'])])
# hosts.add([python_hosts.HostsEntry(entry_type='ipv4',address='23.67.163.105',names=['arbiter.warframe.com'])])
hosts.write()

print("Start login in")
for i in tqdm.trange(700):
    time.sleep(0.01)

for i in range(0, 50):
    if (isProcessRunning("Warframe.x64")):
        try:
            app = Application().connect(title="Warframe")
            app['Warframe'].wait('visible')
        except:
            time.sleep(2)
        break
    else:
        time.sleep(2)

print("Get focus and enter password")
time.sleep(5)
app['Warframe'].click_input(button='left', coords=(870, 445))
app['Warframe'].type_keys("fjb123.")
app['Warframe'].type_keys("{ENTER}")
print("Login Success!")
for i in tqdm.trange(2000):
    time.sleep(0.01)

print("Get daily bonus")
for i in range(2):
    app['Warframe'].click_input(button='left', coords=bounsCoords1)
    time.sleep(0.3)
    app['Warframe'].press_mouse(button='left', coords=bounsCoords2)
    time.sleep(0.3)
for i in tqdm.trange(100):
    time.sleep(0.01)
os.system("taskkill /f /im Warframe.x64.exe")
hosts.remove_all_matching(address='23.67.163.105')
hosts.write()
print("Done")
time.sleep(2)
