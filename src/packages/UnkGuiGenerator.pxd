cimport LanguageManager
cimport GuiManager
cimport Constants


cpdef comboTransUpdate(GuiManager.GuiManager gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addTrans(GuiManager.GuiManager gui, tab)
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)

cpdef comboFusUpdate(GuiManager.GuiManager gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addFusion(GuiManager.GuiManager gui, tab)
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)

cpdef updateScrollbar(canvas, event, int width=*, int height=*)
    # type: (tk.Canvas, tk.Event, int, int) -> None

cpdef onActiveRowClick(GuiManager.GuiManager gui, button, tuple pos)
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, tuple) -> None

cpdef onActiveMenuOn(GuiManager.GuiManager gui, button, tuple pos)
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, tuple) -> None

cpdef comboMenusUpdate(GuiManager.GuiManager gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addMenusTab(GuiManager.GuiManager gui, tab)
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)
