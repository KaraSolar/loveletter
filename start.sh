#!/bin/bash
source env/bin/activate
python3 main.py 2>&1 | gawk '{print strftime("%Y-%m-%d %H:%M:%S"), $0; fflush() }' | tee -a output.log
