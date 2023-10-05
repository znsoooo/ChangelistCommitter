import wx
import git


class CommitBox(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.massage = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.author  = wx.TextCtrl(self)
        self.email   = wx.TextCtrl(self)
        self.amend   = wx.CheckBox(self, -1, 'Amend')
        self.commit  = wx.Button(self, -1, 'Commit')

        box = wx.BoxSizer(wx.VERTICAL)

        box.Add(self.massage, 1, wx.ALL | wx.EXPAND)
        box.Add(self.author,  0, wx.ALL | wx.EXPAND)
        box.Add(self.email,   0, wx.ALL | wx.EXPAND)
        box.Add(self.amend,   0, wx.ALL | wx.EXPAND)
        box.Add(self.commit,  0, wx.ALL | wx.EXPAND)

        self.SetSizer(box)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, size=(400, 400))

    tree = CommitBox(frame)

    frame.Center()
    frame.Show()
    app.MainLoop()
