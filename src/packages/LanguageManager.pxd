# import sqlite3

cdef class LanguageManager:
    cdef str dbname
    cdef str dbFolder
    # cdef sqlite3.Connection connection
    # cdef sqlite3.Cursor cursor
    cdef connection
    cdef cursor


    cpdef list getCharactersNames(self)
        # type: () -> list

    cpdef list getAnimations(self)
        # type: () -> list

    cpdef list getAuras(self)
        # type: () -> list

    cpdef list getR3Command(self)
        # type: () -> list

    cpdef list getTransformationBonus(self)
        # type: () -> list

    cpdef list getFusionsTypes(self)
        # type: () -> list


    cpdef int getCharactersNamesID(self, str name)
        # type: (str) -> int

    cpdef int getAnimationsID(self, str name)
        # type: (str) -> int

    cpdef int getAurasID(self, str name)
        # type: (str) -> int

    cpdef int getR3CommandID(self, str name)
        # type: (str) -> int

    cpdef int getTransformationBonusID(self, str name)
        # type: (str) -> int

    cpdef int getFusionsTypesID(self, str name)
        # type: (str) -> int


    cpdef int getCharactersNamesPos(self, int ide)
        # type: (int) -> int

    cpdef int getAnimationsPos(self, int ide)
        # type: (int) -> int

    cpdef int getAurasPos(self, int ide)
        # type: (int) -> int

    cpdef int getR3CommandPos(self, int ide)
        # type: (int) -> int

    cpdef int getTransformationBonusPos(self, int ide)
        # type: (int) -> int

    cpdef int getFusionsTypesPos(self, int ide)
        # type: (int) -> int


    cdef executeScriptsFromFile(self, str filename)
        # type: (str) -> None

    cpdef close(self)
        # type: () -> None
