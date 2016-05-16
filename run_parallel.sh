#!/bin/bash

#SBATCH --job-name=ipypar-workers
#SBATCH --partition=compute
#SBATCH --mem-per-cpu=8g
#SBATCH --ntasks=101

#SBATCH --mail-user=shhong@oist.jp

#SBATCH --output=/work/DeSchutterU/shhong/joboutputs/%j.out.log
#SBATCH --error=/work/DeSchutterU/shhong/joboutputs/%j.err.log

######### FOR RUNNING IN THE OIST CLUSTER WITH IPYPARALLEL

echo 'HOME =' $HOME
echo 'PATH =' $PATH
echo 'LD_LIBRARY_PATH =' $LD_LIBRARY_PATH
echo 'DISPLAY = ' $DISPLAY
unset DISPLAY

cd $SLURM_SUBMIT_DIR
echo 'WORKDIR =' $SLURM_SUBMIT_DIR

NENGS=$(($SLURM_NTASKS - 1))
echo 'NENGS = ' $NENGS

IPYTHONDIR=$SLURM_SUBMIT_DIR/$SLURM_JOB_ID.ipython
echo $IPYTHONDIR

ipython profile create --ipython-dir=$IPYTHONDIR
ipcontroller --ip='*' --ipython-dir=$IPYTHONDIR &

sleep 10

srun ipengine --ipython-dir=$IPYTHONDIR

# &
# sleep 25
#
# IPYTHONDIR=$IPYTHONDIR python optimize_navrsg.py
#
# sleep 25
#
# rm -rf $IPYTHONDIR

# # log completed job in .err file
# echo "[${SLURM_JOB_NAME}_${SLURM_JOB_ID} completed]"
