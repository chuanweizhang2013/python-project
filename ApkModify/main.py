
import wx
from modify_view import ModifyFrame

if __name__ == '__main__':
    app = wx.App(False)
    frame = ModifyFrame()
    frame.Show()
    app.MainLoop()