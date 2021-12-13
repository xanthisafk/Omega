#!/bin/sh
FILE=./config.json
if [ -f "$FILE" ]; then
    pip install -r requirements.txt
    cd files
    sudo -s java -jar lavalink.jar
    cd ..
    python main.py
else
    python setup.py
fi