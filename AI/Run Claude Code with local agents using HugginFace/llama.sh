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
        --parallel 1 \
        --ctx-size 131072

    # Qwen has context of 32k (32,768)
    # GPT-OSS has context of 128k (131,072)
    # Gemma4 has context of 128k (131,072)
}


# serve unsloth/Qwen3.5-9B-GGUF IQ4_NL Qwen3.5-Q8
# serve unsloth/gpt-oss-20b-GGUF Q8_0 GPT-OSS-Q8
# serve unsloth/gemma-4-E4B-it-GGUF BF16 Gemma4 # 15.1 GB
serve unsloth/gemma-4-E4B-it-GGUF Q8_0 Gemma4 # 8.19 GB
