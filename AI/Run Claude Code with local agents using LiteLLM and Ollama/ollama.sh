#!/bin/sh
set -e

echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama API..."
until ollama list >/dev/null 2>&1; do
  sleep 1
done
echo "Ollama server ready"

# Loop over each model in the list
IFS=',' # comma as separator
for MODEL in $MODELS; do
  MODEL=$(echo "$MODEL" | xargs)
  if ! ollama list | grep -q "$MODEL"; then
    echo "Pulling model $MODEL..."
    ollama pull "$MODEL"
  else
    echo "Model $MODEL already present"
  fi
done

echo "Ollama running with models $MODELS"
wait $OLLAMA_PID
