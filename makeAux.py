from distutils import sysconfig
import sys
import os
import shutil
import zipfile


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


def folderExists(folder):
    # type: (str) -> bool
    return os.path.isdir(folder)


def getDirectory(folders):
    return os.path.join(*folders)


def getMkdir(folders):
    folder = getDirectory(folders)
    if not folderExists(os.path.join(os.getcwd(), folder)):
        print("mkdir ", folder)
        os.mkdir(os.path.join(os.getcwd(), folder))
    return


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
    return


def getPythonDll():
    # type: () -> list
    try:
        import win32process
    except ImportError:
        print("No module. Install: https://sourceforge.net/projects/pywin32/files/pywin32/")
        raise
    dll = list()

    for process in win32process.EnumProcessModules(-1):
        name = win32process.GetModuleFileNameEx(-1, process)
        # print(name)
        if "python" in name and name.endswith(".dll"):
            dll.append(name)
    return dll


def copyPythonDependencies():
    pyFolder = getPythonFolder()
    DLLs = ["_sqlite3.pyd", "_tkinter.pyd"]
    for dllFile in os.listdir(os.path.join(pyFolder, "DLLs")):
        fileRoute = os.path.join(pyFolder, "DLLs", dllFile)
        if os.path.isfile(fileRoute) and fileRoute.lower().endswith(".dll"):
            DLLs.append(dllFile)

    folders = ["DLLs", "tcl", "logs"]

    for x in folders:
        mkdir = os.path.join(os.getcwd(), "out", x)
        if folderExists(mkdir):
            print("rm", mkdir)
            shutil.rmtree(mkdir)
        print("mkdir", mkdir)
        os.mkdir(mkdir)
    dependencies = [(os.path.join("DLLs", x), os.path.join("DLLs", x)) for x in DLLs]
    for dirName in os.listdir(os.path.join(pyFolder, "tcl")):
        if folderExists(os.path.join(pyFolder, "tcl", dirName)):
            lowered = dirName.lower()
            if (lowered.startswith("tcl") or lowered.startswith("tk")) and "." in lowered:
                dependencies.append((os.path.join("tcl", dirName), os.path.join("tcl", dirName)))

    for depend in dependencies:
        src = os.path.join(pyFolder, depend[0])
        dst = os.path.join(os.getcwd(), "out", depend[1])
        print("cp " + src + " " + dst)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, dst)

    if not folderExists(os.path.join(os.getcwd(), "Lib")):
        os.mkdir(os.path.join(os.getcwd(), "Lib"))

    LibDependencies = ['abc.py', 'codecs.py', 'functools.py', 'genericpath.py',
                       'heapq.py', 'keyword.py', 'linecache.py', 'ntpath.py', 'os.py', 're.py', 'sre_compile.py',
                       'sre_constants.py', 'sre_parse.py', 'stat.py', 'traceback.py', 'types.py',
                       'warnings.py', '_weakrefset.py', '__future__.py']

    LibDependenciesFolder = ['encodings', 'sqlite3']

    ver = getPythonVersion()[0]
    if ver == 2:
        LibDependencies += ['collections.py', 'copy_reg.py', 'UserDict.py', '_abcoll.py']
        LibDependenciesFolder += ['lib-tk']
    elif ver == 3:
        LibDependencies += ['copyreg.py', 'io.py', 'site.py', '_collections_abc.py', '_sitebuiltins.py', 'sysconfig.py',
                            'operator.py', 'reprlib.py', 'weakref.py', 'enum.py', 'fnmatch.py', 'posixpath.py',
                            'datetime.py', 'tokenize.py']
        LibDependenciesFolder += ["collections", "tkinter"]
    else:
        # dunno
        LibDependencies += ['copyreg.py', 'io.py', 'site.py', '_collections_abc.py', '_sitebuiltins.py', 'sysconfig.py',
                            'operator.py', 'reprlib.py', 'weakref.py', 'enum.py', 'fnmatch.py', 'posixpath.py',
                            'datetime.py', 'tokenize.py']
        LibDependenciesFolder += ["collections", "tkinter"]

    destination = os.path.join(os.getcwd(), "Lib/")
    for i in LibDependencies:
        srcFile = os.path.join(pyFolder, "Lib", i)
        print("cp", srcFile, destination, "\n")
        shutil.copy2(srcFile, destination)
        outFile = os.path.join(os.getcwd(), "Lib", i)
        # py_compile.compile(outFile)
        # os.remove(outFile)

    for i in LibDependenciesFolder:
        libFolder = os.path.join(os.getcwd(), "Lib", i)
        if not folderExists(libFolder):
            os.mkdir(libFolder)
        for j in os.listdir(os.path.join(pyFolder, "Lib", i)):
            if os.path.isfile(os.path.join(pyFolder, "Lib", i, j)) and j.endswith(".py"):
                print("cp", os.path.join(pyFolder, "Lib", i, j), os.path.join(os.getcwd(), "Lib", i))
                shutil.copy2(os.path.join(pyFolder, "Lib", i, j), os.path.join(os.getcwd(), "Lib", i))

    zipf = zipfile.ZipFile(os.path.join('out', 'pythonLib.zip'), 'w', zipfile.ZIP_DEFLATED)
    zipdir('Lib', zipf)
    zipf.close()

    shutil.rmtree(os.path.join(os.getcwd(), "Lib"))
    return


def copyWindowsData():
    if isWindows():
        dlls = getPythonDll()
        for dll in dlls:
            shutil.copy2(dll, os.path.join(os.getcwd(), "out"))

        copyPythonDependencies()

        src = os.path.join(os.getcwd(), "src", "start.bat")
        out = os.path.join(os.getcwd(), "out")
        shutil.copy2(src, out)
    return


def copyProjectFiles():
    dst = os.path.join(os.getcwd(), "out", "lang")
    if folderExists(dst):
        shutil.rmtree(dst)
    langFolder = os.path.join(os.getcwd(), "lang")
    print("\tcp", langFolder, dst)
    shutil.copytree(langFolder, dst)

    dst = os.path.join(os.getcwd(), "out", "resources")
    if folderExists(dst):
        shutil.rmtree(dst)
    resourcesFolder = os.path.join(os.getcwd(), "resources")
    print("\tcp", resourcesFolder, dst)
    shutil.copytree(resourcesFolder, dst)
    return


def getPydDirs(pydSearchingDir, outputDir, pydFiles, pydDirs):
    for pyd in os.listdir(pydSearchingDir):
        if os.path.isfile(os.path.join(pydSearchingDir, pyd)) and pyd.lower().endswith(".pyd"):
            if pyd not in pydFiles:
                tupla = (os.path.join(pydSearchingDir, pyd), outputDir)
                pydDirs.append(tupla)
                pydFiles.append(pyd)
    return


def copyBinaryFiles():
    pydFiles = list()
    pydDirs = list()
    outFolder = os.path.join(os.getcwd(), "out")
    srcFolder = os.path.join(os.getcwd(), "src")
    packagesFolder = os.path.join("packages")
    c_librariesFolder = os.path.join(packagesFolder, "c_libraries")
    getPydDirs(os.path.join(srcFolder, c_librariesFolder), packagesFolder, pydFiles, pydDirs)
    getPydDirs(os.path.join(srcFolder, packagesFolder), packagesFolder, pydFiles, pydDirs)
    getPydDirs(srcFolder, "", pydFiles, pydDirs)

    import src.makeAux
    finalName = src.makeAux.getFinalName()
    if isWindows():
        finalName += ".exe"
    pydFiles.append(finalName)
    pydDirs.append((finalName, ""))

    for copy in pydDirs:
        copySrc = os.path.join(srcFolder, copy[0])
        copyOut = os.path.join(outFolder, copy[1])
        print("\tcp", copySrc, copyOut)
        shutil.copy2(copySrc, copyOut)
    return


def copyFiles():
    getMkdir([os.getcwd(), 'out'])
    copyProjectFiles()
    copyWindowsData()
    copyBinaryFiles()

    return 0
