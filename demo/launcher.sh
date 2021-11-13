#!/bin/bash
python3 -m pip install git+https://github.com/glspi/gcli-cfgrepo.git
git clone https://github.com/glspi/temp-cfgrepo.git
cd temp-cfgrepo
cfgrepo load