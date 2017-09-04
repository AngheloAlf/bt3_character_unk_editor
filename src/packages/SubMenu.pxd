cimport StatMenu
cimport Constants


cdef tuple getMenuName(str submenuData, int i)
    # type: (str, int) -> (list, int)

cdef tuple getStat(str submenuData, int i)
    # type: (str, int) -> (StatMenu.StatMenu, int)


cdef class SubMenu:
    cdef list menuName
    cpdef public list stats

    cpdef bint isNone(self)
        # type: () -> bool

    cpdef void setMenuNum(self, int num)
        # type: (int) -> None

    cpdef int getMenuNum(self)
        # type: () -> int

    cpdef unicode getMenuName(self)
        # type: () -> unicode

    cpdef void setMenuName(self, unicode name)
        # type: (unicode) -> None

    cpdef str getAsLine(self)
        # type: () -> str