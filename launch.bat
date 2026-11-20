@echo off
title MOOC Studio - Autonomous Course Producer
cd /d "%~dp0"

echo ===================================================
echo     MOOC STUDIO: ONE-CLICK PRODUCTION ENGINE
echo ===================================================

python main.py %1

if exist "workspace\output\Lecture_01.mp4" (
    explorer "workspace\output"
)

pause
