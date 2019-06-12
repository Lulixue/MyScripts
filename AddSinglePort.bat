@echo off

set VM=%1
set port=%2
set priority=%3
echo Open Port: %2 with priority %3
az vm open-port -g Development -n %VM% --port %port% --priority %priority%