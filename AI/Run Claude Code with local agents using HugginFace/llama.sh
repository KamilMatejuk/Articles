serve() {
    local model=$1
    local prec=$2
    local alias=$3

    /app/llama-server \
        -hf "$model:$prec" \
        --alias "$alias" \
        --port 11434 \
        --jinja \
        --kv-unified \
        --cache-type-k q8_0 \
        --cache-type-v q8_0 \
        --flash-attn on \
        --batch-size 2048 \
        --ubatch-size 512 \
        --ctx-size 32768
}


# serve bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF Q4_K_M DeepSeek-Coder-Q4
# serve bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF Q8_0 DeepSeek-Coder-Q8

# serve unsloth/Qwen3-Coder-Next-GGUF UD-TQ1_0 Qwen3-Coder-Next-Q1
# serve unsloth/Qwen3-Coder-Next-GGUF UD-IQ2_XXS Qwen3-Coder-Next-Q2
# serve unsloth/Qwen3-Coder-Next-GGUF IQ4_NL Qwen3-Coder-Next-Q4

# serve unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF Q3_K_M Qwen3-Coder-Q3
# serve unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF Q4_0 Qwen3-Coder-Q4

# serve unsloth/Qwen3.5-9B-GGUF IQ4_NL Qwen3.5-Q4
# serve unsloth/Qwen3.5-9B-GGUF Q8_0 Qwen3.5-Q8
# serve unsloth/Qwen3.5-9B-GGUF UD-Q8_K_XL Qwen3.5-U8

# serve unsloth/gpt-oss-20b-GGUF Q4_K_M GPT-OSS-Q4
serve unsloth/gpt-oss-20b-GGUF Q8_0 GPT-OSS-Q8
# serve unsloth/gpt-oss-20b-GGUF F16 GPT-OSS-F16
