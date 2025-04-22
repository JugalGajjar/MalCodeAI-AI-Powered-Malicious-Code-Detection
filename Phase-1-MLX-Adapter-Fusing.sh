#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
ADAPTER_PATH="Phase-1-Adapters"
SAVE_DIR="./Phase-1-MLX-Fine-Tuned"
OUTPUT_LOG_FILE="Phase-1-MLX-Adapter-Fusing-Log.txt"

# COMMAND
python -m mlx_lm.fuse \
    --model "$MODEL" \
    --save-path "$SAVE_DIR" \
    --adapter-path "$ADAPTER_PATH" \
    | tee "$OUTPUT_LOG_FILE"