#!/bin/bash
#SBATCH --mem=30G
#SBATCH -N 1
#SBATCH -p RM-shared
#SBATCH -t 60:00:00
#SBATCH --ntasks-per-node=8


IMAGE="/home/bshrestha/projects/Tfunck/neuromaps-dev-env/neuromaps.sif"

dir=/home/bshrestha/projects


apptainer exec \
    --bind $dir:$dir \
    $IMAGE \
    /bin/bash