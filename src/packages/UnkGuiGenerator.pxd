cimport LanguageManager
cimport GuiManager
cimport OptionsManager
cimport Constants


cpdef void comboTransUpdate(GuiManager.GuiManager gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addTrans(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

cpdef void comboFusUpdate(GuiManager.GuiManager gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addFusion(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

cpdef void updateScrollbar(canvas, event, int width=*, int height=*)
    # type: (tk.Canvas, tk.Event, int, int) -> None

cpdef void onActiveRowClick(GuiManager.GuiManager gui, button, tuple pos)
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, tuple) -> None

cpdef void onActiveMenuOn(GuiManager.GuiManager gui, button, tuple pos)
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, tuple) -> None

cpdef void comboMenusUpdate(GuiManager.GuiManager gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addMenusTab(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

cpdef tuple optionsTab(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)
