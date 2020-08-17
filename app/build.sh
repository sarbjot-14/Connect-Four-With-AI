#!/bin/sh

set -e

swig -python -py3 -modern example.i
gcc -fPIC -c example.c example_wrap.c -I/usr/include/python3.5
ld -shared example.o example_wrap.o -o _example.so
python3 fact.py
python3 mandel.py
