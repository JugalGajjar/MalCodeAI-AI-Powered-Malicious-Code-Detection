#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
ADAPTER_PATH="Phase_1_Adapters_200Iter"
SAVE_DIR="./Phase_1_MLX_Fine_Tuned"
OUTPUT_LOG_FILE="./Phase_1_Logs/Phase_1_MLX_adapter_fusing_log_200iter.txt"

# COMMAND
python -m mlx_lm.fuse \
    --model "$MODEL" \
    --save-path "$SAVE_DIR" \
    --adapter-path "$ADAPTER_PATH" \
    | tee "$OUTPUT_LOG_FILE"