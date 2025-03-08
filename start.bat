@echo off
title EduBang
setlocal enabledelayedexpansion

type edubang_ascii.txt

for /f "delims=" %%P in ('where python') do set "python_paths=!python_paths! %%P"

set "latest_version="
for %%P in (%python_paths%) do (
    set "current_version=%%P"
    if "!latest_version!"=="" set "latest_version=!current_version!"
    if "!current_version!" gtr "!latest_version!" set "latest_version=!current_version!"
)

set PYTHON_PATH=%latest_version%

%PYTHON_PATH% -m pip install -r requirements.txt
%PYTHON_PATH% ./sources/main.py
