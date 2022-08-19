'''
Author       : Primimy
Date         : 2022-07-27 00:12:51
'''
from pywinauto.application import Application
import os
from pywinauto import mouse
from pywinauto import keyboard
import win32api
main = "C:/Program Files (x86)/WOMic/WOMicClient.exe"
os.popen(main)
app = Application().connect(path="C:/Program Files (x86)/WOMic/WOMicClient.exe")
app['WO MIC Client'].menu_select("连接 ->连接...")
app['建立连接'].连接.click()
app['WO MIC Client'].minimize()