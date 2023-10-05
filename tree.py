import wx
import wx.lib.agw.customtreectrl as ct

import git


class Tree(ct.CustomTreeCtrl):
    def __init__(self, parent):
        ct.CustomTreeCtrl.__init__(self, parent)
        self.Bind(ct.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    def OnChecked(self, evt):
        item = evt.GetItem()
        self.SetItem3State(item, False)
        self.SetChildrenValue(item)
        self.SetParentValue(item)
        self.Refresh()

    def SetChildrenValue(self, item):
        value = item.GetValue()
        for child in item.GetChildren():
            child.Set3StateValue(value)
            self.SetChildrenValue(child)

    def SetParentValue(self, item):
        parent = item.GetParent()
        if parent:
            children = {item.GetValue() for item in parent.GetChildren()}
            if children in [{1}, {0}]:
                self.SetItem3State(parent, False)
                parent.Set3StateValue(children.pop())
            else:
                self.SetItem3State(parent, True)
                parent.Set3StateValue(2)
            self.SetParentValue(parent)


class FilelistTree(Tree):
    def __init__(self, parent):
        Tree.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)

    def SetFilelist(self, top, paths):
        self.DeleteAllItems()
        root = self.AddRoot(top, 1)
        for path in paths:
            node = root
            for part in path.split('/'):
                for child in node.GetChildren():
                    if child.GetData() == part:
                        node = child
                        break
                else:
                    node = self.AppendItem(node, part, 1, data=part)
        self.ExpandAll()


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, size=(300, 600))

    tree = FilelistTree(frame)
    tree.SetFilelist(git.toplevel().strip(), git.changelist().splitlines())

    frame.Center()
    frame.Show()
    app.MainLoop()
