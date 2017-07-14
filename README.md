# bt3_character_unk_editor
BT3 character 'unk' editor

## Compilation:

`python setup.py make`

* Flag `-a` generates html cython files

* Flag `-Wall` is passed to `gcc`


## clean:

* `python setup.py clean`
    * deletes the '.c', '.pyc' and '.html' files.
* `python setup.py cleanAll`
    * invokes `clean` and removes the compilated files.

## Dependencies:

* cython
	* pip install Cython
	
* python-tk

### Windows:

* gcc
     * [mingw32](http://www.mingw.org/)
     
* [win32process](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/)
