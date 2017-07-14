# from distutils.core import setup
# from Cython.Build import cythonize
import os
from distutils import sysconfig
import sys
from subprocess import Popen, PIPE
# from distutils.extension import Extension


def runProcess(proc, showCommand=False):
    # type: (list, bool) -> int
    if showCommand:
        print " ".join(proc)
    try:
        process = Popen(proc, stdout=PIPE)
        # process = Popen(proc)
        (output, err) = process.communicate()
        return process.wait()
    except WindowsError, err:
        print "\tFatal error", err.errno, ": " + proc[0] + "not found"
        exit(err.errno)
    # TODO: que tipo de error ocurre en linux


def getPythonIncludeFolder():
    # type: () -> str
    return sysconfig.get_python_inc()


def getLIBPL():
    # type: () -> str
    LIBPL = sysconfig.get_config_var('LIBPL')
    if not LIBPL:
        if sys.platform == "win32":
            LIBPL = "C:\\Python27\\libs"
        else:
            print "sysconfig.get_config_var('LIBPL') returned None"
            exit(1)
    return LIBPL


def getLIBS():
    # type: () -> list
    LIBS = sysconfig.get_config_var('LIBS')

    if not LIBS:
        if sys.platform == "win32":
            LIBS = "-lpython27 -lpthread"
        else:
            print "sysconfig.get_config_var('LIBS') returned None"
            exit(1)

    if sys.platform == "linux2":
        LIBS = LIBS.split(" ")[:-2]
    elif sys.platform == "win32":
        LIBS = LIBS.split(" ")
    else:
        LIBS = LIBS.split(" ")

    return LIBS


def getPYLIBRARY():
    # type: () -> str
    PYLIB = sysconfig.get_config_var('LIBRARY')
    if not PYLIB:
        if sys.platform == "win32":
            PYLIB = "m"
        else:
            print "sysconfig.get_config_var('LIBRARY') returned None"
            exit(1)

    if sys.platform == "linux2":
        PYLIB = PYLIB[3:-2]
    elif sys.platform == "win32":
        pass
        # PYLIB = sysconfig.get_config_var('LIBRARY')[3:-2]
    else:
        PYLIB = PYLIB[3:-2]
    return PYLIB


def getPythonDll():
    # type: () -> list
    import win32process
    dll = list()

    for process in win32process.EnumProcessModules(-1):
        name = win32process.GetModuleFileNameEx(-1, process)
        # print name
        if "python" in name and name.endswith(".dll"):
            dll.append(name)
    return dll


# def compilePyPackages():
#     packagesFolder = os.path.join("src", "packages")
#     pyFiles = [(f[:-3], os.path.join(packagesFolder, f)) for f in os.listdir(packagesFolder) if
#                os.path.isfile(os.path.join(packagesFolder, f)) and f.lower().endswith(".py") and f != "__init__.py"]

#     for py in pyFiles:
#         setup(name=py[0], ext_modules=cythonize([py[1]]))

#     open(os.path.join("packages", "__init__.py"), "w").close()

#     return 0


def compilePyPackages(arguments):
    packagesFolder = os.path.join("src", "packages")
    pyFiles = [(f[:-3], os.path.join(packagesFolder, f)) for f in os.listdir(packagesFolder) if
               os.path.isfile(os.path.join(packagesFolder, f)) and f.lower().endswith(".py") and f != "__init__.py"]

    if not os.path.isdir(os.path.join(os.getcwd(), 'out')):
        mkdir = ["mkdir", "out"]
        exit_code = runProcess(mkdir, True)
        if exit_code:
            print "Error creating the folder 'out'"
            exit(exit_code)
        mkdir = ["mkdir", os.path.join("out", "packages")]
        exit_code = runProcess(mkdir, True)
        if exit_code:
            print "Error creating the folder 'out\\packages'"
            exit(exit_code)
    elif not os.path.isdir(os.path.join(os.getcwd(), 'out', 'packages')):
        mkdir = ["mkdir", os.path.join("out", "packages")]
        exit_code = runProcess(mkdir, True)
        if exit_code:
            print "Error creating the folder 'out\\packages'"
            exit(exit_code)

    pythonInclude = getPythonIncludeFolder()
    LIBPL = getLIBPL()
    LIBS = getLIBS()

    cy = ["cython", ""]
    if "-a" in arguments:
        cy.append("-a")

    compileCommand = ["gcc", "-shared", "-fPIC", "-fno-strict-aliasing", "-I", pythonInclude, "-L", LIBPL, "-o", "", ""]
    compileCommand += LIBS
    if "-Wall" in arguments:
        compileCommand.append("-Wall")

    for py in pyFiles:
        # setup(name=py[0], ext_modules=cythonize([py[1]]))
        soName = os.path.join("out", "packages", py[0])
        cName = os.path.join(packagesFolder, py[0] + ".c")
        if sys.platform == "win32":
            soName += ".pyd"
        else:
            soName += ".so"

        cy[1] = py[1]
        # cy = ["cython", py[1]]
        exit_code = runProcess(cy, True)
        if exit_code:
            print "Error 'cythonize " + py[1] + "'"
            exit(exit_code)

        # compileCommand = ["gcc", "-shared", "-fwrapv", "-fno-strict-aliasing", "-I", pythonInclude, "-L", LIBPL, "-o",
        #                   soName, cName] + LIBS
        # compileCommand = ["gcc", "-shared", "-fPIC", "-fno-strict-aliasing", "-I", pythonInclude, "-L", LIBPL, "-o",
        #                   soName, cName] + LIBS

        compileCommand[9] = soName
        compileCommand[10] = cName

        exit_code = runProcess(compileCommand, True)
        if exit_code:
            print "error 'gcc " + cName + "'"
            exit(exit_code)

        print ""

    open(os.path.join("out", "packages", "__init__.py"), "w").close()

    return 0


def mainPyToC(arguments):
    cythonizeCommand = ["cython", "--embed", "-o", "src/main.c", "src/main.py"]
    if "-a" in arguments:
        cythonizeCommand.append("-a")
    return runProcess(cythonizeCommand, True)


def cToBinary(arguments):
    pythonInclude = getPythonIncludeFolder()
    LIBPL = getLIBPL()
    LIBS = getLIBS()
    PYLIBRARY = getPYLIBRARY()

    # compileCommandList = ["gcc", "-Os", "-I", pythonInclude, "-L", LIBPL, "-o", finalName, "src/main.c"] + LIBS + \
    #                      ["-l" + PYLIBRARY]
    compileCommandList = ["gcc", "-I", pythonInclude, "-L", LIBPL]
    compileCommandList += ["-o", os.path.join("out", finalName), "src/main.c"]
    compileCommandList += LIBS + ["-l" + PYLIBRARY]
    if "-Wall" in arguments:
        compileCommandList.append("-Wall")
    # compileCommandList = ["gcc", "-I", pythonInclude, "-L", LIBPL, "-o", os.path.join("out", finalName), "src/main.c"] + \
    #                      LIBS + ["-l" + PYLIBRARY]
    return runProcess(compileCommandList, True)


def parseArg(arg):
    if arg in sys.argv:
        sys.argv.remove(arg)
        return [arg]
    return list()


def argv():
    # l = list()
    returned = list()
    # if 'build_ext' not in sys.argv:
    #     l.append('build_ext')
    # if '--inplace' not in sys.argv:
    #     l.append('--inplace')

    # if sys.platform == "win32":
    #    if '--compiler=mingw32' not in sys.argv:
    #        l.append('--compiler=mingw32')

    returned += parseArg("make")
    returned += parseArg("clean")
    returned += parseArg("cleanAll")
    returned += parseArg("-a")
    returned += parseArg("-Wall")

    # sys.argv = [sys.argv[0]] + l + sys.argv[1:]
    return returned


def copyFiles():
    if not os.path.isdir(os.path.join(os.getcwd(), 'out')):
        mkdir = ["mkdir", "out"]
        exit_code = runProcess(mkdir, True)
        if exit_code:
            print "Error creating the folder 'out'"
            exit(exit_code)

    copy = ["cp", "-a", "lang/", "out/"]
    exit_code = runProcess(copy, True)

    # move = ["mv", "packages", "out"]
    # exit_code += runProcess(move, True)

    # if sys.platform == "win32":
    #     move = ["mv", finalName + ".exe", "out"]
    # else:
    #     move = ["mv", finalName, "out"]
    # exit_code += runProcess(move, True)

    if sys.platform == "win32":
        dlls = getPythonDll()
        for dll in dlls:
            copy = ["cp", dll, "out/"]
            exit_code += runProcess(copy, True)

    return exit_code


def makeAll(arguments):
    print "\tcompiling packages -> 'shared object'"
    compilePyPackages(arguments)
    print "\t'shared object' files ready\n\n"

    print "\tmain.py -> main.c"
    exit_code = mainPyToC(arguments)
    if exit_code:
        print "Error embedding the main.py"
        exit(exit_code)
    print "\tmain.c ready\n\n"

    print "\tcompiling main.c -> binary"
    exit_code = cToBinary(arguments)
    if exit_code:
        print "Error compilling main.c"
        exit(exit_code)
    print "\tmain.c->binary ready\n\n"

    print "\tcopying files -> out/"
    exit_code = copyFiles()
    if exit_code:
        print "Error copying files"
        exit(exit_code)
    print "\tfiles copied\n\n"


def clean(arguments):
    rmMain = ["rm", os.path.join("src", "main.c")]
    exit_code = runProcess(rmMain, True)

    # rmBuild = ["rm", "-r", "build"]
    # exit_code += runProcess(rmBuild, True)

    packagesFolder = os.path.join("src", "packages")
    rmFiles = [os.path.join(packagesFolder, f) for f in os.listdir(packagesFolder)
               if os.path.isfile(os.path.join(packagesFolder, f)) and
               (f.lower().endswith(".pyc") or f.lower().endswith(".c")) or f.lower().endswith(".html")]
    for delete in rmFiles:
        rmPac = ["rm", delete]
        exit_code += runProcess(rmPac, True)

    return exit_code


def cleanAll(arguments):
    exit_code = clean(arguments)

    # if sys.platform == "win32":
    #     rmMain = ["rm", finalName + ".exe"]
    # else:
    #     rmMain = ["rm", finalName]
    # exit_code += runProcess(rmMain, True)
    #
    # rmPac = ["rm", "-r", "packages"]
    # exit_code += runProcess(rmPac, True)

    rm = ["rm", "-r", "out"]
    exit_code += runProcess(rm, True)

    return exit_code


def main():
    args = argv()

    if 'make' in args:
        makeAll(args)

    if 'clean' in args:
        clean(args)

    if 'cleanAll' in args:
        cleanAll(args)

    if 'make' not in args and 'clean' not in args and 'cleanAll' not in args:
        print "\tmake\n\tclean\n\tcleanAll\n"

    print "\n\tREADY"

finalName = "bt3_character_unk_editor"

if __name__ == "__main__":
    main()

