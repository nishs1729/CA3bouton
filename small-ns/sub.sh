#!/bin/bash
ISI=($(seq 80 10 130))

for i in "${ISI[@]}"
do
    qsub -N NSI20V${i} -v I=$i jns.sh
done
