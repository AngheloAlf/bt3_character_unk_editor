# bt3_character_unk_editor
BT3 character 'unk' editor

# Compilation:

python setup.py make

if on windows, mingw is recomended:

python setup.py make --compiler=mingw32


# clean:

python setup.py clean
or
python setup.py cleanAll

clean deletes the '.c' and '.pyc' files and the 'build' folder
cleanAll deletes like clean and removes the compilated files.

# Dependencies:

cython
	pip install Cython

python-tk

gcc
windows:  mingw32
