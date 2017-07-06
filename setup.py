from distutils.core import setup
from Cython.Build import cythonize
import os
import distutils.sysconfig
from distutils import sysconfig
import sys
from subprocess import Popen, PIPE
# from distutils.extension import Extension


def runProcess(proc, showCommand=False):
    # type: (list, bool) -> int
    if showCommand:
        print " ".join(proc)
    process = Popen(proc, stdout=PIPE)
    (output, err) = process.communicate()
    return process.wait()


def getPythonIncludeFolder():
    return distutils.sysconfig.get_python_inc()


def getLIBPL():
    LIBPL = sysconfig.get_config_var('LIBPL')
    if not LIBPL:
        if sys.platform == "win32":
            LIBPL = "C:\\Python27\\libs"
        else:
            print "sysconfig.get_config_var('LIBPL') returned None"
            exit(1)
    return LIBPL


def getLIBS():
    LIBS = distutils.sysconfig.get_config_var('LIBS')

    if not LIBS:
        if sys.platform == "win32":
            LIBS = "-lpython27 -lpthread"
        else:
            print "distutils.sysconfig.get_config_var('LIBS') returned None"
            exit(1)

    if sys.platform == "linux2":
        LIBS = LIBS.split(" ")[:-2]
    elif sys.platform == "win32":
        LIBS = LIBS.split(" ")
    else:
        LIBS = LIBS.split(" ")

    return LIBS


def getPYLIBRARY():
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


def compilePyPackages():
    packagesFolder = os.path.join("src", "packages")
    pyFiles = [os.path.join(packagesFolder, f) for f in os.listdir(packagesFolder) if
               os.path.isfile(os.path.join(packagesFolder, f)) and f.lower().endswith(".py") and f != "__init__.py"]

    for py in pyFiles:
        setup(name=finalName, ext_modules=cythonize([py]))

    open(os.path.join("packages", "__init__.py"), "w").close()

    return 0


def mainPyToC():
    cythonizeCommand = ["cython", "--embed", "-o", "src/main.c", "src/main.py"]
    return runProcess(cythonizeCommand, True)


def cToBinary():
    pythonInclude = getPythonIncludeFolder()
    LIBPL = getLIBPL()
    LIBS = getLIBS()
    PYLIBRARY = getPYLIBRARY()

    compileCommandList = ["gcc", "-Os", "-I", pythonInclude, "-L", LIBPL, "-o", finalName, "src/main.c"] + LIBS + \
                         ["-l" + PYLIBRARY]
    return runProcess(compileCommandList, True)


def argv():
    l = list()
    returned = list()
    if 'build_ext' not in sys.argv:
        l.append('build_ext')
    if '--inplace' not in sys.argv:
        l.append('--inplace')

    # if sys.platform == "win32":
    #    if '--compiler=mingw32' not in sys.argv:
    #        l.append('--compiler=mingw32')

    if 'make' in sys.argv:
        returned.append('make')
        sys.argv.remove('make')
    if 'clean' in sys.argv:
        returned.append('clean')
        sys.argv.remove('clean')
    if 'cleanAll' in sys.argv:
        returned.append('cleanAll')
        sys.argv.remove('cleanAll')
    sys.argv = [sys.argv[0]] + l + sys.argv[1:]
    return returned


def moveFiles():
    if not os.path.isdir(os.path.join(os.getcwd(), 'out')):
        print "no existe"
        mkdir = ["mkdir", "out"]
        exit_code = runProcess(mkdir, True)
        if exit_code:
            print "Error creating the folder 'out'"
            exit(exit_code)

    copy = ["cp", "-a", "lang/", "out/"]
    exit_code = runProcess(copy, True)

    move = ["mv", "packages", "out"]
    exit_code += runProcess(move, True)

    if sys.platform == "win32":
        move = ["mv", finalName + ".exe", "out"]
    else:
        move = ["mv", finalName, "out"]
    exit_code = runProcess(move, True)

    return exit_code


def makeAll():
    print "\n\tcompiling packages->'shared object'\n"
    compilePyPackages()
    print "\n\t'shared object' files ready\n"

    print "\n\tmain.py -> main.c\n"
    exit_code = mainPyToC()
    if exit_code:
        print "Error embedding the main.py"
        exit(exit_code)
    print "\n\tmain.c ready\n"

    print "\n\tcompiling main.c->binary\n"
    exit_code = cToBinary()
    if exit_code:
        print "Error compilling main.c"
        exit(exit_code)
    print "\n\tmain.c->binary ready\n"

    print "\n\tmoving files -> out/\n"
    exit_code = moveFiles()
    if exit_code:
        print "Error moving files"
        exit(exit_code)
    print "\n\tfiles moved\n"


def clean():
    rmMain = ["rm", os.path.join("src", "main.c")]
    exit_code = runProcess(rmMain, True)

    rmBuild = ["rm", "-r", "build"]
    exit_code += runProcess(rmBuild, True)

    packagesFolder = os.path.join("src", "packages")
    rmFiles = [os.path.join(packagesFolder, f) for f in os.listdir(packagesFolder)
               if os.path.isfile(os.path.join(packagesFolder, f)) and
               (f.lower().endswith(".pyc") or f.lower().endswith(".c"))]
    for delete in rmFiles:
        rmPac = ["rm", delete]
        exit_code += runProcess(rmPac, True)

    return exit_code


def cleanAll():
    exit_code = clean()

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


finalName = "bt3_character_unk_editor"
args = argv()

if 'make' in args:
    makeAll()

if 'clean' in args:
    clean()

if 'cleanAll' in args:
    cleanAll()

if 'make' not in args and 'clean' not in args and 'cleanAll' not in args:
    print "\tmake\n\tclean\n\tcleanAll\n"

print "\n\tREADY"
