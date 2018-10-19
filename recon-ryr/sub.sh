#!/bin/bash

freq=($(seq 5 5 40))

for i in "${freq[@]}"
do
    qsub -N rec-RSI20V${i} -v I=$i jryr.sh
done
