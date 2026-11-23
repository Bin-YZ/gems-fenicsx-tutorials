@echo off
rem Run case.yaml in this folder (or the file given as first argument) with the WSL Python of the fenicsx environment.
rem Change the path below to your own environment (see "conda env list" inside WSL).
cd /d "%~dp0"
set "CASE_FILE=%~1"
if not defined CASE_FILE set "CASE_FILE=case.yaml"
wsl /home/xi_b/miniforge3/envs/fenicsx/bin/python coupling.py "%CASE_FILE%"
set "RUN_RESULT=%ERRORLEVEL%"
pause
exit /b %RUN_RESULT%
