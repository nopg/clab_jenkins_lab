#!/bin/bash
python3 -m pip install git+https://github.com/nopg/gcli-cfgrepo.git
git clone https://github.com/nopg/temp-cfgrepo.git
cd temp-cfgrepo
cfgrepo load
