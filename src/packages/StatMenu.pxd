from . cimport StatChars
from . cimport Constants

cdef class StatMenu:
    cdef bytes name
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

    cpdef void setBarrasKi(self, unicode data)
        # type: (str) -> None

    cpdef unicode getReservaKi(self)
        # type: () -> unicode

    cpdef void setReservaKi(self, unicode data)
        # type: (str) -> None

    cpdef list getStatChars(self)
        # type: () -> list

    # cpdef setStatChars(self, list data)

    cpdef bytes getAsLine(self)
        # type: () -> str

