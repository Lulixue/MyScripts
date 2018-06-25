@echo off
set "work_path=."
set dir_no=1
set "TO_NUL= >nul 2>nul"

if "%1" == "cmd" (
	@echo on
	set "TO_NUL="
)

:body
	set "work_path=%~dp0"
	echo. work_path: %work_path%
	call :scan_dir %work_path% 0


goto :END
	
:scan_dir
	set "scan_path=%1"
	set scan_depth=%2
	set /a scan_depth+=1
	echo. scan: %scan_path% [%scan_depth%]
	for /f %%s in ('dir /b %1') do (
		call :do_file %%s %scan_depth% %scan_path%
	)
goto :EOF

REM :: is a wrong label 
REM ::放在复合语句中会发生意想不到的错误

:do_file
	set do_depth=%2
	set "do_path=%3\%1"
	set "do_name=%1"
	set is_dir=0
	
	
	REM judge file is dir or not, solution1
	REM if exist %do_path%\*.* (
		REM set is_dir=1
	REM ) 
	REM solution2
	dir /ad %do_path% >nul 2>nul&& set is_dir=1
	
	echo. depth: %do_depth%
	echo. file: %do_path%[dir:%is_dir%]
	if %is_dir% EQU 0 (
		if %do_depth% GEQ 2 (
			call :do_makefile %do_path%
		)
		goto :EOF
	)
	REM rename dir name as subdir_
	REM delete subdir in dir
	REM set should be out of if statements
	REM 变量赋值最好放在外面,避免出现意想不到的问题
	set do_renamed=0
	set cur_dir_no=%dir_no%
	set new_dir=%do_path%
	set "new_name=subdir_%cur_dir_no%"
	set "new_dir=%3\subdir_%cur_dir_no%"
	
	echo "%do_path%" | find "subdir" >nul && set do_renamed=1
	if %do_depth% LEQ 1 (
		set /a do_depth+=1
		echo. renamed: %do_renamed%
		if %do_renamed% EQU 0 (
			echo. rename dir: %do_name% -^> %new_name%
			rename %do_path% %new_name% 
		)
		call :scan_dir %new_dir% %do_depth% 
		REM this operation show after new_dir scope finished
		REM otherwise there will be mistake
		set /a dir_no += 1
	) else (
		echo. delete dir: %do_path%
		del /s /f /q %do_path% %TO_NUL%
		rmdir /s /q %do_path% 
	)
goto :EOF

:do_makefile
	set "bak_mk=%1_tmp"
	REM read all lines in file 
	REM the whitespaces will be truncated
	for /f "tokens=*" %%s in (%1) do (
		set line=%%s
		set newline=%line:focaltech_touch=my_dir%
		echo. %newline% > %bak_mk%
	)
	del /f /q %1 %TO_NUL%
	rename %bak_mk% Makefile %TO_NUL%

goto :EOF

:END
	pause 