@echo off
if "%1" == "hide" goto :run
start /B "" "%0" hide & exit
:run
python pinkpig.py