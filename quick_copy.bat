@echo off
echo Skapar projektkopia...
echo.

cd /d C:\Users\robin\PycharmProjects\linkdb

set DEST_NAME=linkdb_dev_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%
set DEST_NAME=%DEST_NAME: =0%
set DEST=C:\Users\robin\PycharmProjects\%DEST_NAME%

echo Kopierar till: %DEST%
echo.

xcopy /E /I /H /Y /EXCLUDE:exclude.txt . "%DEST%" > nul 2>&1

echo Skapar README...
(
echo # LinkDB - Utvecklingskopia
echo.
echo Kopierad från: C:\Users\robin\PycharmProjects\linkdb
echo Skapad: %DATE% %TIME%
echo.
echo ## Setup
echo.
echo ```bash
echo python -m venv .venv
echo .venv\Scripts\activate
echo pip install rich openpyxl tldextract
echo ```
) > "%DEST%\README_COPY.md"

echo.
echo ✅ Kopia skapad: %DEST%
echo.
echo Öppnar i File Explorer...
explorer "%DEST%"

pause

