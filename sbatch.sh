#!/bin/bash
#SBATCH --job-name=dsta_versa
#SBATCH --output=dsta_versa.out
#SBATCH --error=dsta_versa.err
#SBATCH --partition=swl_general
#SBATCH --gres=gpu:1
#SBATCH --mem=40G
#SBATCH --cpus-per-task=12
#SBATCH --time=1-00:00:00

# Your job commands go here
conda activate speech_quality
#srun python evaluate_speechbleu_ASVspoof2019.py 
srun python versa/bin/scorer.py \
    --score_config egs/speech_cpu.yaml \
    --gt None \
    --pred dsta-maritime_01.scp \
    --output_file test_result_ch_01_cpu
