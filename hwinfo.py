'''
Author       : Primimy
Date         : 2022-07-27 13:30:33
'''
from turtle import title
import pywinauto
import os
from pywinauto import mouse
from pywinauto import keyboard
from pywinauto import taskbar

app = pywinauto.application.Application().connect(path="explorer")
systray_icons = app.ShellTrayWnd.NotificationAreaToolbar
# systray_icons.ClickSystemTrayIcon("Hwinfo")
taskbar.SystemTrayIcons
app = pywinauto.Application().connect(title="Hwinfo")
app.RightClickSystemTrayIcon("Hwinfo")