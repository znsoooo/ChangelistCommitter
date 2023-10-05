import wx

import git
import tree
import editor
import commit


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.tree = tree.FilelistTree(self)
        self.commit = commit.CommitBox(self)
        self.editor = editor.ParallelEditor(self)

        box1 = wx.BoxSizer(wx.VERTICAL)
        box1.Add(self.tree,   1, wx.ALL | wx.EXPAND)
        box1.Add(self.commit, 1, wx.ALL | wx.EXPAND)

        box = wx.BoxSizer()
        box.Add(box1, 0, wx.ALL | wx.EXPAND)
        box.Add(self.editor, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(box)

        self.commit.commit.Bind(wx.EVT_BUTTON, self.OnCommit)

    def OnCommit(self, evt):
        git.commit()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Commit', size=(1200, 800))
        self.panel = MyPanel(self)
        self.Center()
        self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
