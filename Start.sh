#!/bin/bash
date=`date +%Y/%m/%d`
hour=`date +%H:%M`
timestamp=`date +%Y-%m-%d_%H-%M-%S`

entrada=1
start_restart='Start'
LOGFILE="log/logfileterminal_$timestamp.txt"

touch $LOGFILE
exec > >(tee $LOGFILE) 2>&1
echo "$date"-"$hour" ' - Iniciando o BATCH Start.sh'

while [ $entrada == 1 ] 
do
    echo "$date"-"$hour" " - Aguardando 5s - $start_restart"
    sleep 5

    echo "$date"-"$hour" ' - iniciando o programa'
    python main.py

    return_python=$?
    echo $return_python

    if [ $return_python == 2 ] 
    then
        entrada=0
        echo "$date"-"$hour" " - Finalizando o programa"
    else
        start_restart='Restart'
        echo "$date"-"$hour" " - Restart no programa"
    fi
done