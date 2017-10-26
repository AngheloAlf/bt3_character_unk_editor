CC				:= gcc
SHARED      	:= -shared
SOME_FLAGS      :=  -fPIC -fno-strict-aliasing
PY_INCLUDE		:= "$(shell python -c "import makeAux;print(makeAux.getPythonIncludeFolder())")"
PY_LIBS_DIR		:= "$(shell python -c "import makeAux;print(makeAux.getLIBPL())")"
PY_LIBS			:= $(shell python -c "import makeAux;print(' '.join(makeAux.getLIBS()))")
PY_LIBRARY_M    := $(shell python -c "import  makeAux;print(makeAux.getPYLIBRARY())")

OBJS            = $(shell python -c "import makeAux;print(makeAux.getObjects())")

WIND            := $(shell python -c "import makeAux;print(makeAux.getWindRes())")
WINDCC          := $(shell python -c "import makeAux;print(makeAux.getWindResComp())")

FINAL_NAME      := $(shell python -c "import makeAux;print(makeAux.getFinalName())")

all: main

main:
	cython --embed -o main.c main.py
	python -c "import makeAux;makeAux.fixWinMain('main.c')"
	$(WIND)
	$(CC) -I $(PY_INCLUDE) -L $(PY_LIBS_DIR) -o ../out/$(FINAL_NAME) main.c $(WINDCC) $(PY_LIBS) -l$(PY_LIBRARY_M)
