@echo off
chcp 65001

setlocal

:: Configurar las rutas de VLC y FFmpeg
set "vlc_path=C:\Program Files\VideoLAN\VLC\"

:: Configurar la URL de origen y el nombre base del archivo de salida
set "SOURCE_URL=http://generalrodriguez.gob.ar:8000/radio"
set "OUTPUT_BASE=Programa-Contactos_%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%"

:: Calcular la duración de la grabación en segundos
set /a RECORDING_DURATION=61*60

:: Crear el nombre completo del archivo de salida con el texto adicional
set "OUTPUT_FILE=%OUTPUT_BASE%.mp3"

:: Iniciar la grabación
echo Grabando desde %SOURCE_URL% por %RECORDING_DURATION% segundos...
start /B "" "%VLC_PATH%\vlc.exe" -I dummy %SOURCE_URL% --sout=#transcode{acodec=mp3,ab=128,channels=2,samplerate=44100}:std{access=file,mux=mp3,dst="%OUTPUT_FILE%"} vlc://quit

:: Mostrar la barra de progreso
set /a PROGRESS=0

:LOOP
set /a PROGRESS+=1
set /a MINUTES=PROGRESS/60
set /a SECONDS=PROGRESS%%60
setlocal EnableDelayedExpansion
set "MINUTES=0!MINUTES!"
set "SECONDS=0!SECONDS!"
set "BAR="
set /a PERCENT=PROGRESS*100/RECORDING_DURATION
for /L %%I in (1,1,100) do if %%I LEQ !PERCENT! (set "BAR=!BAR!#") else (set "BAR=!BAR! ")
cls
echo Grabando desde %SOURCE_URL% por %RECORDING_DURATION% segundos...
echo.
echo Tiempo transcurrido: !MINUTES:~-2!:!SECONDS:~-2!
echo !PERCENT!%% [!BAR!]
echo.
endlocal

:: Esperar 1 segundo antes de volver a actualizar la pantalla
ping -n 2 127.0.0.1 >NUL

:: Verificar si la grabación ha terminado
if %PROGRESS% GEQ %RECORDING_DURATION% goto FINISH

:: Volver a actualizar la pantalla
goto LOOP

:FINISH
echo.
echo La grabación ha finalizado. El archivo se ha guardado como "%OUTPUT_FILE%".
pause
REM Cerrar VLC
taskkill /IM vlc.exe /F >nul
exit


