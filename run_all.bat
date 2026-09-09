@echo off
title MoSPI iGOT Karmayogi Launcher
echo ======================================================================
echo Launching MoSPI AI-Enabled Competency Platform (SIH26101)
echo Official iGOT Karmayogi Theme
echo ======================================================================
echo.
echo Launching Backend server in a separate window...
start "MoSPI Backend (Port 8000)" cmd /c run_backend.bat

echo Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul

echo Launching Frontend portal in a separate window...
start "MoSPI Frontend (Port 5173)" cmd /c run_frontend.bat

echo.
echo ======================================================================
echo System successfully initiated!
echo  * Frontend Portal: http://localhost:5173
echo  * Backend API:     http://127.0.0.1:8000
echo  * API Swagger UI:  http://127.0.0.1:8000/docs
echo ======================================================================
echo.
pause
