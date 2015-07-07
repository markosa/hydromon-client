#!/bin/sh
find . -name '*.pyc' -exec rm {} \;
tar cvf hydromon.tar hydromond.py net/ ph/ ec/

