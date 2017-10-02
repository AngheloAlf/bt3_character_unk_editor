@echo off
title start_bt3_character_unk_editor
echo Ejecutando programa
bt3_character_unk_editor.exe
echo La aplicacion termino con codigo de salida: %errorlevel%
pause
exit /b %errorlevel%
