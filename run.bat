@echo off
title TermGuard Server
echo Starting TermGuard - Autonomous Contract & Deadline Defense...
cd /d "%~dp0"
start http://localhost:3000
npm run dev
pause
