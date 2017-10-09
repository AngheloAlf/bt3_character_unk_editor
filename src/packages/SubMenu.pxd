from . cimport StatMenu
from . cimport Constants


cdef StatMenu.StatMenu getStat(bytes submenuData, int i)
    # type: (str, int) -> StatMenu.StatMenu


cdef class SubMenu:
    cdef list menuName
    cpdef public list stats
    cdef bint printData

    cdef list __searchMenuName(self, bytes submenuData)
        # type: (bytes) -> list[bytes]

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

    cpdef bytes getAsLine(self)
        # type: () -> str