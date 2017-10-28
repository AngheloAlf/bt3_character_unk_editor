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

all: packages

packages: $(OBJS)
	 @echo $(OBJS)

%.pyd: %.c
	$(CC) $(SHARED) $(SOME_FLAGS) -I $(PY_INCLUDE) -L $(PY_LIBS_DIR) -o $@ $< $(PY_LIBS)
	rm $<
	@echo

%.c: %.py
	@echo
	cython $< -3
	@echo

clean:
	rm *.pyd
