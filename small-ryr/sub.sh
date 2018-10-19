#!/bin/bash
freq=($(seq 50 10 60))

for i in "${freq[@]}"
do
    qsub -N RSI20V${i} -v I=$i jryr.sh
done
