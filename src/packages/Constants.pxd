cdef class FilesConst:
    cpdef public list menuNameCode
    cpdef public list endOfLine
    cpdef public list statCode
    # cpdef public list numberSign
    cpdef public list transformCode
    cpdef public list startOfMenuFile
    cpdef public list endOfMenuFile
    cpdef public list endOfFile
    cpdef public list startOfutf16Text

cdef class ProgramCons:
    cpdef public unicode Title
    cpdef public unicode Version
    cpdef public tuple FileTypes

cdef class AmountConst:
    cpdef public int statsAmount
    cpdef public int menusAmount
    cpdef public int languagesAmount

cdef class CharsTypes:
    cpdef public str text
    cpdef public str unknown1
    cpdef public str unknown2
    cpdef public str unknown8
    cpdef public str unknown4
    cpdef public str unknownD

cpdef str hexListToChar(list hexList)
    # type: (list) -> str

# cpdef list findDataPos(str archivo, str data, int maxi=*, int inicio=*, int tope=*)
    # type: (str, str, int, int, int) -> list
