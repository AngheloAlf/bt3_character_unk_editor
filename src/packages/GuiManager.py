import os
try:
    import Tkinter as tk
    import ttk
    import tkFileDialog
    import tkMessageBox
except Exception:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox


def popupInfo(title, text):
    # type: (unicode, unicode) -> None
    tkMessageBox.showinfo(title, text)


def popupWarning(title, text):
    # type: (unicode, unicode) -> None
    tkMessageBox.showwarning(title, text)


def popupError(title, text):
    # type: (unicode, unicode) -> None
    tkMessageBox.showerror(title, text)


# askokcancel(text1, text2) -> bool
# askyesno(a, b) -> bool
#    ask yes or no
# askretrycancel(a, b) -> bool
#    ask "retry" or "cancel". has a warning sign
# askyesnocancel(a, b) -> bool
#    ask yes, no or cancel. returns True, False or None respectively


def addMsgToText(txtWid, msg):
    # type: (tk.Text, str) -> None
    txtWid["state"] = "normal"
    txtWid.insert(tk.END, msg + "\n")
    txtWid.see(tk.END)
    txtWid["state"] = "disabled"


def openFile(title, fileTypes, callback=None):
    # type: (unicode, tuple, (unicode, )) -> unicode
    archivo = unicode(tkFileDialog.askopenfilename(initialdir="/", title=title, filetypes=fileTypes))
    try:
        print(archivo)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(archivo)
    return archivo


def saveFile(title, fileTypes, callback=None):
    # type: (unicode, tuple, (unicode, )) -> unicode
    archivo = unicode(tkFileDialog.asksaveasfilename(initialdir="/", title=title, filetypes=fileTypes))
    try:
        print(archivo)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(archivo)
    return archivo


def selectMultiplesFiles(title, fileTypes, callback=None):
    # type: (unicode, tuple, (unicode, )) -> list[unicode]
    archivos = tkFileDialog.askopenfilenames(initialdir="/", title=title, filetypes=fileTypes)
    if type(archivos) != tuple:
        return list()
    archivos = map(unicode, archivos)
    try:
        print(archivos)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(archivos)
    return archivos


def selectFolder(title=None, callback=None):
    # type: (unicode, (unicode, )) -> unicode
    carpeta = unicode(tkFileDialog.askdirectory(title=title))
    try:
        print(carpeta)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(carpeta)
    return carpeta


def generateTtkWidget(wtype, master, posT, x, y, values=None, width=None, current=None, command=None, **kwargs):
    # type: (unicode, ttk.Frame|ttk.LabelFrame, unicode, int, int, list, int, int, function, **kwargs) ->
    # None|ttk.Label|ttk.Combobox|ttk.Entry|ttk.Button|CheckButton
    if wtype == u"Label":
        widget = ttk.Label(master, **kwargs)
    elif wtype == u"Combobox":
        widget = ttk.Combobox(master, state='disabled', values=values, **kwargs)
        if command:
            widget.bind("<<ComboboxSelected>>", command)
    elif wtype == u"Entry":
        widget = ttk.Entry(master, state='disabled', **kwargs)
    elif wtype == u"Button":
        widget = ttk.Button(master, state="disabled", **kwargs)
    elif wtype == u"CheckButton":
        widget = CheckButton(master, state="disabled", onvalue=1, offvalue=0, **kwargs)
        widget.deselect()
        if command:
            widget["command"] = command
    else:
        return
    if current:
        widget.current(current)
    if posT == u"pack" or posT == u"place":
        widget.pack()
        if width:
            widget.place(x=x, y=y, width=width)
        else:
            widget.place(x=x, y=y)
        widget.place(x=x, y=y)
    elif posT == u"grid":
        if width:
            widget["width"] = width
        widget.grid(row=x, column=y)
    else:
        return
    return widget


class GuiManager:
    def __init__(self, title=u"Tk", languageFile=u"spanish.db", icon=None):
        # type: (unicode, unicode, unicode) -> None
        self.gui = tk.Tk()
        self.tabsWidth = 900
        self.tabsHeight = 0
        self.panelsAmmount = 0
        self.height = 0
        self.width = 210
        self.running = False
        self.title = title
        self.tabs = ttk.Notebook(self.gui)
        self.tabsData = dict()
        self.comboboxs = dict()
        self.entries = dict()
        self.checkbuttons = dict()
        self.buttons = dict()
        self.progressBar = list()
        self.restart = False
        self.languageFile = languageFile
        self.icon = icon

    # def addPanel(self, frameName, labels, inputs, button):
    #     # type: (str, list, list, list) -> GuiManager
    #     frame = ttk.LabelFrame(self.gui, text=frameName)
    #     frame.pack(fill="both", expand="yes", side=tk.LEFT)

    #     yPos = []

    #     # inputs = [("Entry", "DefaultText")]
    #     x = 75
    #     y = 0
    #     for i in range(len(inputs)):
    #         yPos.append(y)
    #         if inputs[i][0] == "Entry":
    #             en = ttk.Entry(frame)
    #             en.insert(0, inputs[i][1])
    #             en.place(x=x, y=y)
    #             self.entries[labels[i]] = en
    #             y += 25
    #         elif inputs[i][0] == "Text":
    #             # sc = tk.Scrollbar(frame)
    #             # sc.place(x=x, y=y)

    #             te = tk.Text(frame, state="normal", width="38", height="12")  # , yscrollcommand = sc.set)
    #             te.insert(tk.INSERT, inputs[i][1])
    #             te.place(x=x, y=y)
    #             # te.pack(side = tk.LEFT, fill = tk.BOTH)
    #             self.entries[labels[i]] = te

    #             # sc.config(command = te.yview)
    #             te["state"] = "disabled"

    #             y += 200
    #             if self.width < 400:
    #                 self.width = 400

    #     # labels = ["ip", "port", "usuario"]
    #     x = 0
    #     for l in range(len(labels)):
    #         la = ttk.Label(frame, text=labels[l])
    #         la.place(x=x, y=yPos[l])

    #     yMax = yPos[-1] + 25

    #     # button = ["logear"]
    #     bu = ttk.Button(frame, text=button[0], command=button[1])
    #     bu.place(x=75, y=yMax+25)

    #     if yMax + 25 > self.height:
    #         self.height = yMax + 50

    #     self.panelsAmmount += 1

    #     return self

    def addTab(self, tabName, tabCallback):
        # type: (unicode, (ttk.Frame, )) -> None
        tab = ttk.Frame(self.tabs)  # , width = self.tabsWidth, height = self.tabsHeight)
        self.tabs.add(tab, text=tabName)
        self.tabsData[tabName] = tab
        newX, newY = tabCallback(tab)

        tab["width"] = newX
        tab["height"] = newY

        if newX > self.tabsWidth:
            self.tabsWidth = newX
        if newY > self.tabsHeight:
            self.tabsHeight = newY
        return

    def addMenu(self, cascadeNames, cascadeData):
        # type: (list, list) -> None
        if len(cascadeNames) != len(cascadeData):
            return
        
        menuVar = tk.Menu(self.gui)

        for i in range(len(cascadeNames)):
            subMenu = tk.Menu(menuVar, tearoff=0)
            for optionName, callback in cascadeData[i]:
                if optionName is None:
                    subMenu.add_separator()
                else:
                    if callback:
                        subMenu.add_command(label=optionName, command=callback)
                    else:
                        subMenu.add_command(label=optionName)
            menuVar.add_cascade(label=cascadeNames[i], menu=subMenu)

        self.gui.config(menu=menuVar)

    def getEntries(self):
        # type: () -> dict
        return self.entries

    def start(self, title=None, icon=None):
        # type: (unicode, unicode) -> None
        if icon:
            self.icon = icon
        if self.icon:
            # TODO: test on linux
            if os.name == 'nt':
                try:
                    self.gui.wm_iconbitmap(bitmap=self.icon)
                    # img = tk.PhotoImage(file=self.icon)
                except Exception:
                    self.gui.wm_iconbitmap(bitmap=os.path.join("..", self.icon))
                    # img = tk.PhotoImage(file=os.path.join("..", self.icon))
                # self.gui.tk.call('wm', 'iconphoto', self.gui._w, img)

        if title:
            self.title = title
        self.gui.title(self.title)

        # self.gui.minsize(self.width * self.panelsAmmount, self.height + 20 + 25)
        self.gui.minsize(self.tabsWidth, self.tabsHeight+25)
        self.running = True
        self.tabs.grid(column=0, row=0)
        self.gui.mainloop()

    def stop(self):
        # type: () -> None
        self.gui.destroy()
        # del self.gui
        self.entries = dict()
        self.panelsAmmount = 0
        self.height = 0
        self.gui = tk.Tk()
        self.running = False

    def isClose(self):
        # type: () -> bool
        return not self.running

    def clean(self):
        # type: () -> None
        pass

    def putProgressBar(self, maxi):
        # type: (int) -> None
        pb = ttk.Progressbar(self.gui, orient="horizontal", length=self.tabsWidth, mode="determinate", maximum=maxi)
        pb.grid(column=0, row=1)
        self.progressBar = [pb, maxi]

    def restartProgressBar(self):
        # type: () -> None
        if self.progressBar:
            self.progressBar[0]["value"] = 0

    def updateProgressBar(self):
        # type: () -> None
        if self.progressBar is None:
            return
        if self.progressBar[0]["value"] > self.progressBar[1]:
            self.progressBar[0]["value"] = 0
        self.progressBar[0]["value"] += 1

    def isRestart(self):
        # type: () -> bool
        return self.restart

    def quit(self):
        # type: () -> None
        self.gui.quit()


class CheckButton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        self.var = kwargs.get('variable', tk.IntVar())
        kwargs['variable'] = self.var
        tk.Checkbutton.__init__(self, *args, **kwargs)

    def is_checked(self):
        # type: () -> bool
        return bool(self.var.get())
