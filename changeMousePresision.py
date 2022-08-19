'''
Author       : Primimy
Date         : 2021-03-23 09:10:57
'''
from pywinauto.application import Application

# opening the Mouse Properties app
app = Application().Start(cmd_line="\"C:/WINDOWS/System32/rundll32.exe\" C:/WINDOWS/System32/shell32.dll,Control_RunDLL C:/WINDOWS/System32/main.cpl")
# app = Application().start("main.cpl")
# accessing tabs in the window
mouseproperties_window = app.Dialog
mouseproperties_tabs = mouseproperties_window.TabControl

# switching to Pointer Options tab
mouseproperties_tabs.select(u'指针选项')

# toggling the Enhance Pointer Position checkbox
checkbox_enhancepointer = mouseproperties_window.CheckBox
checkbox_enhancepointer.click()

# saving changes and closing the app
# button_Apply = mouseproperties_window.应用
# button_Apply.Click()
button_OK = mouseproperties_window.确定
button_OK.click()
app.kill()
