#!/bin/sh

cd tests
python -m unittest discover
pypy -m unittest discover

# kernprof -l ./sip-log-sanitizer.py
# python -m line_profiler sip-log-sanitizer.py.lprof
