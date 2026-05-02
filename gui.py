import tkinter as tk
from tkinter import ttk, filedialog


def buildRoot():
    ROOT = tk.Tk()
    ROOT.title('114514')
    ROOT.geometry('800x600')
    ROOT.minsize(400, 300)

    ROOT.columnconfigure(0, weight=1)
    ROOT.rowconfigure(1, weight=1)

    return ROOT


def buildCanvas(rootWindow):
    BACKGROUND = tk.Frame(rootWindow)
    BACKGROUND.grid(row=1, column=0, sticky='nsew')

    CANVAS = tk.PanedWindow(BACKGROUND, orient="horizontal", sashrelief="raised", sashwidth=4)
    CANVAS.pack(fill="both", expand=True)

    return CANVAS


class NavBar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#d4d4d4', height=36)

        self.grid(row=0, column=0, sticky='ew')
        self.grid_propagate(False)


class NavButton(tk.Button):
    def __init__(self, name: str, menu_callback=None, master=None):
        super().__init__(master, relief='flat', bg='#d4d4d4', activebackground='#3498DB', width=6, bd=0)

        self.bind('<Enter>', self.onEnter)
        self.bind('<Leave>', self.onLeave)
        self.config(text=name)
        self.config(command=lambda: menu_callback(self))

    @staticmethod
    def onEnter(event):
        event.widget.config(bg='#85C1E9')

    @staticmethod
    def onLeave(event):
        event.widget.config(bg='#d4d4d4')


def buildNavBar(rootWindow):
    nav = NavBar(rootWindow)
    buildNavButton(nav)

    return nav


def buildNavButton(navBar):
    NavButton_File = NavButton("文件", Controller.NavButtonFile.menu, navBar)
    NavButton_File.pack(side="left")

    NavButton_Edit = NavButton("编辑", Controller.NavButtonEdit.menu, navBar)
    NavButton_Edit.pack(side="left")

    NavButton_Search = NavButton("搜索", Controller.NavButtonSearch.menu, navBar)
    NavButton_Search.pack(side="left")

    NavButton_View = NavButton("视图", Controller.NavButtonView.menu, navBar)
    NavButton_View.pack(side="left")

    NavButton_Encoding = NavButton("编码", Controller.NavButtonEncoding.menu, navBar)
    NavButton_Encoding.pack(side="left")

    NavButton_Setting = NavButton("设置", Controller.NavButtonSetting.menu, navBar)
    NavButton_Setting.pack(side="left")

    NavButton_Tool = NavButton("工具", Controller.NavButtonTool.menu, navBar)
    NavButton_Tool.pack(side="left")


class FileBrowser(tk.Frame):
    def __init__(self, master: tk.PanedWindow = None):
        super().__init__(master, bg='#f0f0f0')
        if master:
            master.add(self, width=200, minsize=120, stretch='never')


class FileTreeview(ttk.Treeview):
    def __init__(self, master: tk.Frame = None):
        super().__init__(master, show='tree')
        self.bind('<<TreeviewOpen>>', self._on_open)

    def load_directory(self, path):
        self.delete(*self.get_children())
        self._root_path = path
        self._populate_tree('', path)

    def _populate_tree(self, parent, path):
        import os
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if not os.path.isdir(os.path.join(path, e))]
        for d in dirs:
            full = os.path.join(path, d)
            node = self.insert(parent, 'end', iid=full, text=d, open=False)
            self.insert(node, 'end', text='...')
        for f in files:
            self.insert(parent, 'end', text=f)

    def _on_open(self, event):
        node = self.focus()
        children = self.get_children(node)
        if children and self.item(children[0], 'text') == '...':
            self.delete(children[0])
            self._populate_tree(node, node)  # iid 即路径


def buildFileBrowser(canvas):
    file_browser = FileBrowser(canvas)
    tree = FileTreeview(file_browser)
    tree.pack(fill='both', expand=True)

    return file_browser, tree










class WorksSpace(tk.Frame):
    def __init__(self, master: tk.PanedWindow = None):
        super().__init__(master, bg='white')
        if master:
            master.add(self, width=420, minsize=200, stretch='always')


def buildWorkspace(canvas):
    workspace = WorksSpace(canvas)
    tk.Label(workspace, text="工作区", bg='white').pack()

    return workspace







class Auxiliary(tk.Frame):
    def __init__(self, master: tk.PanedWindow = None, **kw):
        super().__init__(master, bg='#f0f0f0')
        if master:
            master.add(self, width=200, minsize=100, stretch='never')


def buildAuxiliar(canvas):
    auxiliar = Auxiliary(canvas)
    tk.Label(auxiliar, text="辅助窗口", bg='#f0f0f0').pack()

    return auxiliar






class Controller:
    class NavButtonFile:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="打开文件", command=Controller.NavButtonFile.file_new)
            menu.add_command(label="打开文件夹", command=Controller.NavButtonFile.file_openFolder)
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def file_open(cls):
            path = filedialog.askopenfilename(
                title="打开文件",
                filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt *.json *.lang *.mcmeta")]
            )
            if path:
                print("选中文件:", path)
                # TODO: 加载到工作区
            return path

        @classmethod
        def file_openFolder(cls):
            path = filedialog.askdirectory(title="选择文件夹")
            if path:
                print("选中目录:", path)
                if cls._tree:
                    cls._tree.load_directory(path)
            return path

        _tree = None  # 由外部注入文件树引用

        @classmethod
        def file_new(cls):
            return 0

        @classmethod
        def file_save(cls):
            return 0

        @classmethod
        def file_saveAs(cls):
            return 0

        @classmethod
        def file_close(cls):
            return 0

        @classmethod
        def file_history(cls):
            return 0

    # WIP
    class NavButtonEdit:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="功能1")
            menu.add_command(label="功能2")
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def example(cls):
            return 0

    # WIP
    class NavButtonSearch:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="功能1")
            menu.add_command(label="功能2")
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def example(cls):
            return 0  # WIP

    # WIP
    class NavButtonView:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="功能1")
            menu.add_command(label="功能2")
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def example(cls):
            return 0

    # WIP
    class NavButtonEncoding:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="功能1")
            menu.add_command(label="功能2")
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def example(cls):
            return 0

    # WIP
    class NavButtonSetting:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="功能1")
            menu.add_command(label="功能2")
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def example(cls):
            return 0

    # WIP
    class NavButtonTool:
        @classmethod
        def menu(cls, button):
            menu = tk.Menu(button, tearoff=0)
            menu.add_command(label="功能1")
            menu.add_command(label="功能2")
            menu.add_separator()
            menu.add_command(label="退出", command=button.winfo_toplevel().quit)
            menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())

        @classmethod
        def example(cls):
            return 0


def Show():
    ROOT = buildRoot()
    buildNavBar(ROOT)

    CANVAS = buildCanvas(ROOT)
    file_browser, tree = buildFileBrowser(CANVAS)
    Controller.NavButtonFile._tree = tree  # 注入文件树引用

    buildWorkspace(CANVAS)
    buildAuxiliar(CANVAS)

    ROOT.mainloop()


if __name__ == '__main__':
    Show()
