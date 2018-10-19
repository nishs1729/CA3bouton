#!/bin/bash
freq=($(seq 5 5 70))

for i in "${freq[@]}"
do
    qsub -N NSI20V${i} -v I=$i jns.sh
done
