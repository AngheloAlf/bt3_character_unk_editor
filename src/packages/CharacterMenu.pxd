cimport SubMenu
cimport Constants

cdef class CharacterMenu:
    cpdef public list subMenus
    cdef bint unknow

    cpdef bint isKnow(self)
        # type: () -> bool

    cpdef str getAsLine(self)
        # type: () -> str
    