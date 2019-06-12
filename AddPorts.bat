@echo on
set "VmName=%1"

echo Open Ports

echo Add SSH
call :AddPort %VmName%  22 100

echo Add TCP992
call :AddPort %VmName%  992 110

echo Add TCP1194 
call :AddPort %VmName%  1194 120

echo Add HTTP
call :AddPort %VmName%  80 130

echo Add HTTPS
call :AddPort %VmName%  443 140

echo Add TCP5555
call :AddPort %VmName%  5555 150

echo Add UDP500
call :AddPort %VmName%  500 160

echo Add UDP4500
call :AddPort %VmName%  4500 170

goto :END

:AddPort
	start AddSinglePort.bat %1 %2 %3
goto :EOF


:END
pause