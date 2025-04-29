#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
ADAPTER_PATH="Phase_1_Adapters_4e_LR"
SAVE_DIR="./Phase_2_MLX_Fine_Tuned"
OUTPUT_LOG_FILE="./Phase_2_Logs/Phase_2_MLX_adapter_fusing_log_lr4e.txt"

# COMMAND
python -m mlx_lm.fuse \
    --model "$MODEL" \
    --save-path "$SAVE_DIR" \
    --adapter-path "$ADAPTER_PATH" \
    | tee "$OUTPUT_LOG_FILE"