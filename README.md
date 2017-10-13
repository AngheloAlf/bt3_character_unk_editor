# bt3_character_unk_editor
BT3 character 'unk' editor

## Compilation:

`python setup.py make`

* Flag `-a` generates html cython files

* Flag `-Wall` is passed to `gcc`

* Flag `-nosite` removes the python dependencie on `nosite.py`


## Execution:

`python setup.py exec`

* Executes the compiled file

* Can be combined with `make` flag to compile and exec  the result:
    * `python setup.py make exec`

## clean:

* `python setup.py clean`
    * deletes the '.c', '.pyc' and '.html' files.
* `python setup.py cleanAll`
    * invokes `clean` and removes the compilated files.

## Dependencies:

* [Python 3.6](https://www.python.org/downloads/)

	
* [python-tk](https://wiki.python.org/moin/TkInter)
    * Ubuntu: `apt-get install python-tk`

* [cython](http://cython.org/#download)
	* `pip install cython`
	
### Windows:

* gcc
     * [mingw32](http://www.mingw.org/)

* make
     * [gnuwin32](http://gnuwin32.sourceforge.net/packages/make.htm)
     
* [win32process](https://sourceforge.net/projects/pywin32/files/pywin32/)
