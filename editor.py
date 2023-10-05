import wx
import wx.stc as stc


def OpenFile(path):
    ens = ['utf-8', 'ansi', 'utf-16']
    for en in ens:
        try:
            with open(path, encoding=en) as f:
                return en, f.read()
        except UnicodeDecodeError:
            pass
    return None, "Binary file can't read"


class Editor(stc.StyledTextCtrl):
    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(self, parent)

        self.path = self.encoding = self.text = None

        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'face:Courier New,size:11')
        self.StyleSetSpec(1, 'back:#FFFF00')
        self.StyleSetSpec(2, 'back:#00FFFF')

        self.SetAdditionalSelectionTyping(True)
        self.SetEOLMode(stc.STC_EOL_LF)  # fix save file '\r\n' translate to '\r\r\n'
        self.SetMultipleSelection(True)
        self.SetTabWidth(4)
        self.SetUseTabs(False)
        self.SetViewWhiteSpace(True)

        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 50)
        self.SetMargins(5, 5)

        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginWidth(2, 20)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,     stc.STC_MARK_BOXPLUS,  "white", "#808080")

        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(stc.EVT_STC_CHANGE, self.OnStcChange)
        self.OnStcChange(-1)

    def OnSetFocus(self, evt):
        self.SetFile(self.path)
        evt.Skip()

    def OnStcChange(self, evt):
        lines = self.GetLineCount()
        width = len(str(lines)) * 9 + 5
        self.SetMarginWidth(1, width)
        self.SaveFile()

    def SaveFile(self):
        if self.encoding:
            with open(self.path, 'w', encoding=self.encoding) as f:
                f.write(self.GetValue())

    def SetFile(self, path):
        self.path = path
        ln = self.GetScrollPos(1)
        pos = self.GetInsertionPoint()
        self.encoding, self.text = OpenFile(self.path)
        self.SetValue(self.text)
        self.Enable(bool(self.encoding))
        self.ScrollToLine(ln)
        self.SetInsertionPoint(pos)


class ParallelEditor(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.left  = Editor(self)
        self.right = Editor(self)

        box = wx.BoxSizer()
        box.Add(self.left,  1, wx.ALL | wx.EXPAND)
        box.Add(self.right, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(box)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, size=(1500, 800))
    editor = ParallelEditor(frame)
    editor.left.SetFile(__file__)
    editor.right.SetFile(__file__)
    frame.Center()
    frame.Show()
    app.MainLoop()
