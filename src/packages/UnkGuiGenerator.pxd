from . cimport LanguageManager
from . cimport GuiManager
from . cimport Constants
from . cimport OptionsManager


cpdef void comboTransUpdate(GuiManager.GuiManager gui, event)
# cpdef void comboTransUpdate(gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addTrans(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
# cpdef tuple addTrans(gui, tab, conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

cpdef void comboFusUpdate(GuiManager.GuiManager gui, event)
# cpdef void comboFusUpdate(gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addFusion(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
# cpdef tuple addFusion(gui, tab, conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

cpdef void updateScrollbar(canvas, event, int width=*, int height=*)
    # type: (tk.Canvas, tk.Event, int, int) -> None

cpdef void onActiveRowClick(GuiManager.GuiManager gui, button, tuple pos)
# cpdef void onActiveRowClick(gui, button, tuple pos)
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, tuple) -> None

cpdef void onActiveMenuOn(GuiManager.GuiManager gui, button, tuple pos)
# cpdef void onActiveMenuOn(gui, button, tuple pos)
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, tuple) -> None

cpdef void comboMenusUpdate(GuiManager.GuiManager gui, event)
# cpdef void comboMenusUpdate(gui, event)
    # type: (GuiManager.GuiManager, tk.Event) -> None

cpdef tuple addMenusTab(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
# cpdef tuple addMenusTab(gui, tab, conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

cpdef tuple optionsTab(GuiManager.GuiManager gui, tab, OptionsManager.OptionsManager conf)
# cpdef tuple optionsTab(gui, tab, conf)
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)
