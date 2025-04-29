#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
DATA="./Phase_2_Data"
LR="4e-5"
ITERATIONS="100"
FINE_TUNE_TYPE="lora"
MAX_SEQ_LEN="3072"
NUM_LAYERS="6"
OUTPUT_LOG_FILE="./Phase_2_Logs/Phase_2_MLX_training_log_lr4e.txt"

# COMMAND
python -m mlx_lm.lora \
    --model "$MODEL" \
    --train \
    --data "$DATA" \
    --learning-rate "$LR" \
    --iters "$ITERATIONS" \
    --num-layers "$NUM_LAYERS" \
    --fine-tune-type "$FINE_TUNE_TYPE" \
    --max-seq-length "$MAX_SEQ_LEN" \
    | tee "$OUTPUT_LOG_FILE"
