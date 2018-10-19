#!/bin/bash

#PBS -p -1
#PBS -j oe
#PBS -J 1-1000:1

/apps/bin/mcell /home/nishant/recon-ryr/RS20p20hz.mdl -seed ${PBS_ARRAY_INDEX}
