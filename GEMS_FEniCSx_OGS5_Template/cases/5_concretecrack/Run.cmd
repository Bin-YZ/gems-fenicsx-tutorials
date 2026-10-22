@echo off
wsl.exe -d Ubuntu --cd "%~dp0." --exec /home/xi_b/miniforge3/envs/fenicsx/bin/python -u run_case.py
pause
