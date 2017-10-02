cdef class FilesConst:
    cpdef public bytes menuNameCode
    cpdef public bytes endOfLine
    cpdef public bytes statCode
    # cpdef public list numberSign
    cpdef public bytes transformCode
    cpdef public bytes startOfMenuFile
    cpdef public bytes endOfMenuFile
    cpdef public bytes endOfFile
    cpdef public bytes startOfutf16Text

cdef class ProgramCons:
    cpdef public unicode Title
    cpdef public unicode Version
    cpdef public tuple FileTypes

cdef class AmountConst:
    cpdef public int statsAmount
    cpdef public int menusAmount
    cpdef public int languagesAmount

cdef class CharsTypes:
    cpdef public bytes text
    cpdef public bytes unknown1
    cpdef public bytes unknown2
    cpdef public bytes unknown8
    cpdef public bytes unknown4
    cpdef public bytes unknownD

# cpdef list findDataPos(str archivo, str data, int maxi=*, int inicio=*, int tope=*)
    # type: (str, str, int, int, int) -> list
