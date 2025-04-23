#!/bin/bash

# VARIABLES
MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"
ADAPTER_PATH="Phase-2-Adapters"
SAVE_DIR="./Phase-2-MLX-Fine-Tuned"
OUTPUT_LOG_FILE="Phase-2-MLX-Adapter-Fusing-Log.txt"

# COMMAND
python -m mlx_lm.fuse \
    --model "$MODEL" \
    --save-path "$SAVE_DIR" \
    --adapter-path "$ADAPTER_PATH" \
    | tee "$OUTPUT_LOG_FILE"