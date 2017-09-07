cimport StatChars
cimport Constants

cdef class StatMenu:
    cdef str name
    cdef list data  #MaxPower, BarrasKiOcupa, KiOcupa
    cdef list statChars

    cpdef unicode getName(self)
        # type: () -> unicode

    cpdef void setName(self, unicode name)
        # type: (unicode) -> None

    cpdef int getMaxPower(self)
        # type: () -> int

    cpdef void setMaxPower(self, int data)
        # type: (int) -> None

    cpdef unicode getBarrasKi(self)
        # type: () -> unicode

    cpdef void setBarrasKi(self, str data)
        # type: (str) -> None

    cpdef unicode getReservaKi(self)
        # type: () -> unicode

    cpdef void setReservaKi(self, str data)
        # type: (str) -> None

    cpdef list getStatChars(self)
        # type: () -> list

    # cpdef setStatChars(self, list data)

    cpdef str getAsLine(self)
        # type: () -> str

