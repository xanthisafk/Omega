@echo off
title Omega Bot Instance
IF EXIST "config.py" (
    start /WAIT pip install -r requirements.txt
    cd files
    start java -jar lavalink.jar
    cd ..
    start python main.py
) ELSE (
    start /WAIT python setup.py
    start /WAIT pip install -r requirements.txt
    cd files
    start java -jar lavalink.jar
    cd ..
    start python main.py
)

