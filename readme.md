# A simple c compiler made in python

![tests](https://github.com/Dpbm/python-c-compiler/actions/workflows/tests.yml/badge.svg)

This is a college project that I've done with some friends of mine. 
Feel free to add things, messy around, and test as you want. 
If you find some improvements or bugs, please, `open an Issue` and then us know what's wrong.

## Run

To run the project you'll need:

* python3 installed
* a `c` source code file

after that, just run:

```bash
python3 compiler.py your_file.c
```

## Tests

To execute the tests, you'll need:

* python3
* python unittest
* make (optional)

with all dependencies installed, run:

```
make test

or 

python3 -m unittest tests/*.py
```
