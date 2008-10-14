#coding=utf-8
#!/usr/bin/env python


import wx
import sys
import os.path
import settings 

from windows.frames import MainFrame
from windows.dialogs import CreateUserDialog
from django.core.management import setup_environ

if __name__ == '__main__':
    app = wx.PySimpleApp()
    from resource import res
    
    if len(sys.argv) == 1:
        dlg = CreateUserDialog()
        if dlg.ShowModal() == wx.IDOK:
            pass
        else:
            sys.exit(1)
    else:
        file = os.path.join(os.getcwd(), sys.argv[1])
    if os.path.isfile(file):
        settings.DATABASE_NAME = file
        setup_environ(settings)
        frame = MainFrame()
        frame.Show()
        app.MainLoop()
    else:
        sys.stderr.write(u"错误:未能找到指定的文件<%s>\n" % file)
        sys.exit(1)
