from . cimport SubMenu
from . cimport Constants

cdef class CharacterMenu:
    cpdef public list subMenus
    cdef bint unknow
    cdef bint printData

    cpdef bint isKnow(self)
        # type: () -> bool

    cpdef bytes getAsLine(self)
        # type: () -> bytes
    