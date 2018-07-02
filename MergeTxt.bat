@echo off
set "all_in_one=all.txt"
set "TO_NUL= >NUL 2>NUL"

if "%1" == "cmd" (
	@echo on
	set "TO_NUL="
)
:body
	del /f /q %all_in_one% %TO_NUL%
	ren index.txt 00.txt %TO_NUL%
	for /l %%a in (1 1 9) do ren %%a.txt 0%%a.txt %TO_NUL%
	call :scan_dir .

goto END


:scan_dir
	set "scan_path=%1"
	set /a scan_depth+=1
	echo. scan: %scan_path% 
	for /f %%s in ('dir /b /on %1') do (
		call :do_file %%s 
	)
goto :EOF


:do_file
	set file=%1
	echo. %file:~-4% of %file%
	if %file% == %all_in_one% (
		goto :EOF
	)
	if not "%file:~-4%" == ".txt" (
		goto :EOF
	)
	
	echo. >> %all_in_one%
	REM type %file% ^> %all_in_one%
	for /f "tokens=*" %%s in (%file%) do (
		echo. %%s >> %all_in_one%
	)

goto :EOF

:END
pause