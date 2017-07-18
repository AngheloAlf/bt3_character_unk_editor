cdef class TransformClass:
    cdef str unknowFirst
    cdef list trans, barras, aniCam, aura, abs
    cdef str command, bonus

    # def getR3Command(self, asOrd=False):
        # type: (bool) -> int|str

    # def setR3Command(self, command, asOrd=False):
        # type: (int|str, bool) -> bool

    cpdef list getTransformData(self, int charNumb, bint asOrd=*)
        # type: (int, bool) -> list

    cpdef bint setTransformData(self, int charNumb, list data, bint asOrd=*)
        # type: (int, list, bool) -> bool

    # def getBonus(self, asOrd=False):
        # type: (bool) -> int|str

    # def setBonus(self, bonus, asOrd=False):
        # type: (int|str, bool) -> bool

    cpdef list getAsLines(self)
        # type: () -> list

