#!/bin/bash
#SBATCH --mem=30G
#SBATCH -N 1
#SBATCH -p RM-shared
#SBATCH -t 60:00:00
#SBATCH --ntasks-per-node=8


IMAGE="/ocean/projects/med250004p/bshresth/projects/tfunck/neuromaps-dev-env/neuromaps-workbench.sif"

dir=/ocean/projects/med250004p/bshresth/projects


apptainer exec \
    --bind $dir:$dir \
    $IMAGE \
    /bin/bash