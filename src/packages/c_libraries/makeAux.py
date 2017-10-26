from distutils import sysconfig
import sys
import os
import shutil


def isWindows():
    # type: () -> bool
    return sys.platform == "win32"


def isLinux():
    # type: () -> bool
    return sys.platform.startswith("linux")


def getPythonFolder():
    # type: () -> str
    return os.path.join(*os.path.split(sys.executable)[:-1])


def getPythonVersion():
    # type: () -> tuple
    return sys.version_info[:2]


def getPythonIncludeFolder():
    # type: () -> str
    return sysconfig.get_python_inc()


def getLIBPL():
    # type: () -> str
    LIBPL = sysconfig.get_config_var('LIBPL')
    if not LIBPL:
        if isWindows():
            LIBPL = os.path.join(getPythonFolder(), "libs")
        else:
            print("sysconfig.get_config_var('LIBPL') returned None")
            exit(1)
    return LIBPL


def getLIBS():
    # type: () -> list
    LIBS = sysconfig.get_config_var('LIBS')

    if not LIBS:
        if isWindows():
            version = getPythonVersion()
            LIBS = "-lpython"
            LIBS += "".join(map(str, version))
            LIBS += " -lpthread"
        else:
            print("sysconfig.get_config_var('LIBS') returned None")
            exit(1)

    if isLinux():
        LIBS = LIBS.split(" ")[:-2]
    elif isWindows():
        LIBS = LIBS.split(" ")
    else:
        LIBS = LIBS.split(" ")

    return LIBS


def getObjects():
    cFiles = [f[:-2]+".pyd"
              for f in os.listdir(os.getcwd())
              if os.path.isfile(os.path.join(os.getcwd(), f)) and f.lower().endswith(".c") and f != "main.c"]
    return " ".join(cFiles)


def copyPydFiles():
    for f in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(), f)) and f.lower().endswith(".pyd"):
            print("cp", f, os.path.join("..", f))
            shutil.copy(f, os.path.join("..", f))
    return
