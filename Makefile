CC				:= gcc
SHARED      	:= -shared
SOME_FLAGS      :=  -fPIC -fno-strict-aliasing
PY_INCLUDE		:= "$(shell python -c "import makeAux;print(makeAux.getPythonIncludeFolder())")"
PY_LIBS_DIR		:= "$(shell python -c "import makeAux;print(makeAux.getLIBPL())")"
PY_LIBS			:= $(shell python -c "import makeAux;print(' '.join(makeAux.getLIBS()))")

OBJS            = $(shell python -c "import makeAux;print(makeAux.getObjects())")

MAKE_SRC        := $(shell python -c "import makeAux;print(makeAux.getDirectory(['src']))")
MAKE_PACKAGES   := $(shell python -c "import makeAux;print(makeAux.getDirectory(['src', 'packages']))")
MAKE_C_LIBRARIES:= $(shell python -c "import makeAux;print(makeAux.getDirectory(['src', 'packages', 'c_libraries']))")


all: packages

packages: packagesDir
	@echo
	@echo
	make -C $(MAKE_SRC)
	@echo
	@echo
	make -C $(MAKE_PACKAGES)
	@echo
	@echo
	make -C $(MAKE_C_LIBRARIES)
	@echo
	@echo
	python -c "import makeAux;makeAux.copyProjectFiles()"
	@echo
	@echo
	python -c "import makeAux;makeAux.copyWindowsData()"
	@echo
	@echo
	python -c "import makeAux;makeAux.copyBinaryFiles()"
	@echo
	@echo

outDir:
	python -c "import makeAux;makeAux.getMkdir(['out'])"

packagesDir: outDir
	python -c "import makeAux;makeAux.getMkdir(['out', 'packages'])"

clean:
	rm -r out/

cleanAll: clean
	make -C $(MAKE_SRC) cleanAll
	make -C $(MAKE_PACKAGES) clean
	make -C $(MAKE_C_LIBRARIES) clean
