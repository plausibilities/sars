#!/bin/bash

# A script file for Google Colaboratory

# TeX
# apt-get install texlive-latex-extra  &> tex.log
# apt-get install ghostscript &>> tex.log
# apt-get install dvipng &>> tex.log

# logs
rm -rf *.log

# ArViz & PyMC3
pip install arviz &> arviz.log
pip install pymc3==3.9.3 &> pymc3.log

# https://linux.die.net/man/1/wget
wget -q https://github.com/plausibilities/sars/raw/develop/sars.zip

# https://linux.die.net/man/1/unzip
rm -rf sars
unzip -u -q sars.zip
rm -rf sars.zip