CC				:= gcc
SHARED      	:= -shared
SOME_FLAGS      :=  -fPIC -fno-strict-aliasing
PY_INCLUDE		:= "$(shell python -c "import makeAux;print(makeAux.getPythonIncludeFolder())")"
PY_LIBS_DIR		:= "$(shell python -c "import makeAux;print(makeAux.getLIBPL())")"
PY_LIBS			:= $(shell python -c "import makeAux;print(' '.join(makeAux.getLIBS()))")

OBJS            = $(shell python -c "import makeAux;print(makeAux.getObjects())")
## EXES            = main.exe

all: packages

## packages: ${EXES} ${OBJS}
packages: ${EXES} ${OBJS}
	@echo
	@echo Success

%.pyd: %.o Py3_%.o
	@echo
	$(CC) $(SHARED) $(SOME_FLAGS) -I $(PY_INCLUDE) -L $(PY_LIBS_DIR) -o $@ Py3_$< $< $(PY_LIBS)
	@echo

%.o: %.c
	@echo
	@echo $<
	$(CC) $(SOME_FLAGS) -I $(PY_INCLUDE) -L $(PY_LIBS_DIR) -c $< $(PY_LIBS)
	@echo

%.exe: %.c
	$(CC) $(SOME_FLAGS) -I $(PY_INCLUDE) -L $(PY_LIBS_DIR) -o $@ $< $(PY_LIBS)

clean:
	rm *.pyd *.o
