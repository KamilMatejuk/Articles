#!/bin/sh
set -e

echo "Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

# Wait until API is ready
until curl -sf http://localhost:${PORT_OLLAMA}/api/tags > /dev/null; do sleep 1; done
echo "Ollama ready. Warming up model in GPU memory..."

# Minimal inference to force GPU load
curl -s http://localhost:${PORT_OLLAMA}/api/generate \
  -d "{
    \"model\": \"${MODEL_OLLAMA}\",
    \"prompt\": \"warmup\",
    \"options\": { \"num_predict\": 1, \"temperature\": 0 }
  }" > /dev/null
echo "Model warmed up and resident in GPU."

# Keep Ollama in foreground
wait "$OLLAMA_PID"
