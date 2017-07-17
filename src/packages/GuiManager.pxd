cpdef popUp(str title, str text, str text2)
    # type: (str, str, str) -> None

cpdef showPopUp(str text1, str text2)
    # type: (str, str) -> None

cpdef addMsgToText(txtWid, str msg)
    # type: (Tkinter.Text, str) -> None

cdef class GuiManager:
    cdef gui
    # gui = Tkinter.Tk()
    cdef int tabsWidth
    cdef int tabsHeight
    cpdef dict entries
    cdef int panelsAmmount
    cdef int height
    cdef int width
    cdef bint running
    cdef str title
    cdef tabs
    # tabs = ttk.Notebook(self.gui)
    cdef dict tabsData
    cdef dict comboboxs
    cdef dict checkbuttons
    cdef dict buttons
    cdef list progressBar
    cdef bint restart

    cpdef addTab(self, str  tabName, tabCallback)
        # type: (str, (ttk.Frame, dict, dict, dict, dict)) -> None

    cpdef addMenu(self, list cascadeNames, list cascadeData)
        # type: (list, list) -> None

    cpdef dict getEntries(self)
        # type: () -> dict

    cpdef start(self, str title=*)
        # type: (str) -> None

    cpdef stop(self)
        # type: () -> None

    cpdef bint isClose(self)
        # type: () -> bool

    cpdef unicode openFile(self, str title, tuple fileTypes, callback=*)
        # type: (str, tuple, (unicode, dict, dict, dict, dict)) -> unicode

    cpdef unicode saveFile(self, str title, tuple fileTypes, callback=*)
        # type: (str, tuple, (unicode, dict, dict, dict, dict)) -> unicode

    cpdef unicode openMultiplesFiles(self, str title, tuple fileTypes, callback=*)
        # type: (str, tuple, (unicode, dict, dict, dict, dict)) -> unicode

    cpdef unicode selectFolder(self, str title=*, callback=*)
        # type: (str, (unicode, dict, dict, dict, dict)) -> unicode

    cpdef putProgressBar(self, int maxi)
        # type: (int) -> None

    cpdef restartProgressBar(self)
        # type: () -> None

    cpdef updateProgressBar(self)
        # type: () -> None

    cpdef bint isRestart(self)
        # type: () -> bool

    cpdef quit(self)
        # type: () -> None
