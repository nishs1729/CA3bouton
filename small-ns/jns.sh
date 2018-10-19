#!/bin/bash

#PBS -p 1
#PBS -j oe
#PBS -J 1-1000:1

#/apps/bin/mcell /home/nishant/small-ns/NSI20V${I}.mdl -seed ${PBS_ARRAY_INDEX}

/apps/bin/mcell /home/nishant/small-ns/NS20p20hz.mdl -seed     ${PBS_ARRAY_INDEX}

