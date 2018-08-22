@echo off
REM enable embeded expansion !%%!
setlocal ENABLEDELAYEDEXPANSION

set "DestExt=.jpg"
set "DestStr=."
set "BatFile=%0"

for /f "delims=" %%t in ('dir /b') do (
	call :rename_file %%t
)

goto END

:has_ext
	set "test_str=%1"
	set "dest_str=%2"
	set hasExt=0
	set count=0 
	
	call :get_length %test_str%
	for /l %%a in (0,1,%count%) do (
		if "!test_str:~%%a,1!" == "%dest_str%" set hasExt=1
	)
goto :EOF

REM get string length
:get_length 
	set "mystr=%1"
	set /a count+=1 
	for /f %%i in ("%count%") do if not "!mystr:~%%i,1!"=="" goto get_length %mystr%
goto :eof 

:rename_file
	set "filename=%1"
	
	call :has_ext %filename% %DestStr%
	echo. %filename%[%count%] hasExt: %hasExt%
	
	REM jump if bat file
	if "%filename%" == "%BatFile%" (
		echo.^> current bat file, jump!
		goto :EOF
	)
	
	if %hasExt% EQU 0 (
		rename %filename% %filename%%DestExt%
	)
	
goto :EOF

:END
pause