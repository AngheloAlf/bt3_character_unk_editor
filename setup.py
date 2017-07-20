import os
from distutils import sysconfig
import sys
from subprocess import Popen, PIPE
import zipfile
import py_compile


def runProcess(proc, showCommand=False):
    # type: (list, bool) -> int
    if showCommand:
        print " ".join(proc)
    try:
        process = Popen(proc, stdout=PIPE)
        # process = Popen(proc)
        (output, err) = process.communicate()
        return process.wait()
    except OSError as err:
        print "\tFatal error " + str(err.errno) + ": " + proc[0] + " not found"
        exit(err.errno)


def isWindows():
    # type: () -> bool
    return sys.platform == "win32"


def isLinux():
    # type: () -> bool
    return sys.platform.startswith("linux")


def getPythonIncludeFolder():
    # type: () -> str
    return sysconfig.get_python_inc()


def getLIBPL():
    # type: () -> str
    LIBPL = sysconfig.get_config_var('LIBPL')
    if not LIBPL:
        if isWindows():
            LIBPL = "C:\\Python27\\libs"
        else:
            print "sysconfig.get_config_var('LIBPL') returned None"
            exit(1)
    return LIBPL


def getLIBS():
    # type: () -> list
    LIBS = sysconfig.get_config_var('LIBS')

    if not LIBS:
        if isWindows():
            LIBS = "-lpython27 -lpthread"
        else:
            print "sysconfig.get_config_var('LIBS') returned None"
            exit(1)

    if isLinux():
        LIBS = LIBS.split(" ")[:-2]
    elif isWindows():
        LIBS = LIBS.split(" ")
    else:
        LIBS = LIBS.split(" ")

    return LIBS


def getPYLIBRARY():
    # type: () -> str
    PYLIB = sysconfig.get_config_var('LIBRARY')
    if not PYLIB:
        if isWindows():
            PYLIB = "m"
        else:
            print "sysconfig.get_config_var('LIBRARY') returned None"
            exit(1)

    if isLinux():
        PYLIB = PYLIB[3:-2]
    elif isWindows():
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


def getPythonFolder():
    return os.path.split(sys.executable)[0]


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
        if isWindows():
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

    initDir = os.path.join("out", "packages", "__init__.py")
    open(initDir, "w").close()
    py_compile.compile(initDir)
    runProcess(["rm", initDir])

    return 0


def mainPyToC(arguments):
    # type: (list) -> int
    main = os.path.join("src", "main")
    if "-nosite" in arguments:
        zipName = 'pythonLib.zip'
        folders = ["DLLs", "Lib", "tcl", os.path.join("Lib", "sqlite3"), os.path.join("Lib", "lib-tk")]
        pyzip = ['.', zipName]
        for fld in folders:
            pyzip.append(os.path.join(zipName, fld))
        pyzip.append("DLLs")

        arch = open(main + ".py")
        mainData = ""
        for line in arch:
            mainData += line.strip() + ";"
        arch.close()

        arch = open(main + ".c", "w")
        arch.write('#include <Python.h>\n')
        arch.write('\n')
        arch.write('int main(int argc, char *argv[]){\n')
        arch.write('    Py_NoSiteFlag = 1;\n')
        arch.write('    Py_SetPythonHome(".");\n')
        arch.write('    Py_InitializeEx(0);\n')
        arch.write('    Py_SetProgramName(argv[0]);\n')
        arch.write('    PySys_SetArgv(argc, argv);\n')
        arch.write('    PyRun_SimpleString("import sys");\n')
        arch.write('    PyRun_SimpleString("sys.path = ' + str(pyzip) + '");\n')
        arch.write('\n')
        arch.write('    PyRun_SimpleString("' + mainData + '");\n')
        arch.write('\n')
        arch.write('    Py_Finalize();\n')
        arch.write('    return 0;\n')
        arch.write('}\n')
        arch.close()
        return 0
    else:
        cythonizeCommand = ["cython", "--embed", "-o", main + ".c", main + ".py"]
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
    compileCommandList += ["-o", os.path.join("out", finalName), os.path.join("src", "main.c")]

    if isWindows():
        resResult = os.path.join("src", "winRc.res")
        rcCompilate = ["windres", os.path.join("src", "winRc.rc"), "-O", "coff", "-o", resResult]
        exit_code = runProcess(rcCompilate, True)
        if exit_code:
            print "Error compilating winRc.rc"
        else:
            compileCommandList.append(resResult)

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
    returned += parseArg("exec")
    returned += parseArg("clean")
    returned += parseArg("cleanAll")
    returned += parseArg("-a")
    returned += parseArg("-Wall")
    returned += parseArg("-nosite")

    # sys.argv = [sys.argv[0]] + l + sys.argv[1:]
    return returned


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def copyPythonDependencies():
    folder = getPythonFolder()
    DLLs = ["_sqlite3.pyd", "_tkinter.pyd", "sqlite3.dll", "tcl85.dll", "tk85.dll"]
    tcl85 = ["encoding/"]
    tk85 = ["ttk/"]
    folders = ["DLLs", "tcl", os.path.join("tcl", "tcl8.5"), os.path.join("tcl", "tk8.5")]
    [runProcess(["mkdir", os.path.join("out", x)]) for x in folders]
    dependencies = [(os.path.join("DLLs", x), os.path.join("DLLs", x)) for x in DLLs]
    dependencies += [(os.path.join("tcl", "tcl8.5", x), os.path.join("tcl", "tcl8.5")) for x in tcl85]
    dependencies += [(os.path.join("tcl", "tcl8.5", x), os.path.join("tcl", "tcl8.5", x)) for x in
                     os.listdir(os.path.join(folder, "tcl", "tcl8.5")) if
                     os.path.isfile(os.path.join(folder, "tcl", "tcl8.5", x))]
    dependencies += [(os.path.join("tcl", "tk8.5", x), os.path.join("tcl", "tk8.5")) for x in tk85]
    dependencies += [(os.path.join("tcl", "tk8.5", x), os.path.join("tcl", "tk8.5", x)) for x in
                     os.listdir(os.path.join(folder, "tcl", "tk8.5")) if
                     os.path.isfile(os.path.join(folder, "tcl", "tk8.5", x))]
    for depend in dependencies:
        copy = ["cp", "-r", os.path.join(folder, depend[0]), os.path.join("out", depend[1])]
        if runProcess(copy, True):
            print "\terror: " + " ".join(copy)

    mkdir = ["mkdir", os.path.join("Lib")]
    runProcess(mkdir, True)

    LibDependencies = ['abc.py', 'codecs.py', 'collections.py', 'copy_reg.py', 'functools.py', 'genericpath.py',
                       'heapq.py', 'keyword.py', 'linecache.py', 'ntpath.py', 'os.py', 're.py', 'sre_compile.py',
                       'sre_constants.py', 'sre_parse.py', 'stat.py', 'traceback.py', 'types.py', 'UserDict.py',
                       'warnings.py', '_abcoll.py', '_weakrefset.py']
    LibDependenciesFolder = ['encodings', 'lib-tk', 'sqlite3']

    for i in LibDependencies:
        copy = ["cp", os.path.join(folder, "Lib", i), os.path.join("Lib/")]
        runProcess(copy)
        py_compile.compile(os.path.join("Lib", i))
        rm = ["rm", os.path.join("Lib", i)]
        runProcess(rm)

    for i in LibDependenciesFolder:
        mkdir = ["mkdir", os.path.join("Lib", i)]
        runProcess(mkdir, True)
        for j in os.listdir(os.path.join(folder, "Lib", i)):
            if os.path.isfile(os.path.join(folder, "Lib", i, j)) and j.endswith(".py"):
                copy = ["cp", os.path.join(folder, "Lib", i, j), os.path.join("Lib", i)]
                runProcess(copy, True)
                py_compile.compile(os.path.join("Lib", i, j))
                rm = ["rm", os.path.join("Lib", i, j)]
                runProcess(rm)

    zipf = zipfile.ZipFile(os.path.join('out', 'pythonLib.zip'), 'w', zipfile.ZIP_DEFLATED)
    zipdir('Lib', zipf)
    zipf.close()

    rm = ["rm", "-r", "Lib"]
    runProcess(rm, True)


def copyFiles():
    if not os.path.isdir(os.path.join(os.getcwd(), 'out')):
        mkdir = ["mkdir", "out"]
        exit_code = runProcess(mkdir, True)
        if exit_code:
            print "Error creating the folder 'out'"
            exit(exit_code)

    copy = ["cp", "-a", "lang/", "out/"]
    exit_code = runProcess(copy, True)

    copy = ["cp", "-a", "resources/", "out/"]
    exit_code += runProcess(copy, True)

    if isWindows():
        dlls = getPythonDll()
        exit2 = 0
        for dll in dlls:
            copy = ["cp", dll, "out/"]
            exit2 += runProcess(copy, True)
        if exit2:
            print "\terror copying python dlls"

        copyPythonDependencies()

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


def execBulid(arguments):
    program = os.path.join(os.getcwd(), 'out', finalName)
    if isWindows():
        program += ".exe"
    exit_code = runProcess([program], True)
    if exit_code:
        print "error executing:", program
        exit(exit_code)


def clean(arguments):
    # rmBuild = ["rm", "-r", "build"]
    # exit_code += runProcess(rmBuild, True)

    packagesFolder = os.path.join("src", "packages")
    rmFiles = [os.path.join(packagesFolder, f) for f in os.listdir(packagesFolder)
               if os.path.isfile(os.path.join(packagesFolder, f)) and
               (f.lower().endswith(".pyc") or f.lower().endswith(".c")) or f.lower().endswith(".html")]
    rmFiles += [os.path.join("src", f) for f in os.listdir("src")
                if os.path.isfile(os.path.join("src", f)) and
                (f.lower().endswith(".res") or f.lower().endswith(".c")) or f.lower().endswith(".html")]
    exit_code = 0
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

    if 'exec' in args:
        execBulid(args)

    if 'clean' in args:
        clean(args)

    if 'cleanAll' in args:
        cleanAll(args)

    if 'make' not in args and 'clean' not in args and 'cleanAll' not in args:
        print "\tmake\n\texec\n\tclean\n\tcleanAll\n"

    print "\n\tREADY"


finalName = "bt3_character_unk_editor"

if __name__ == "__main__":
    main()
