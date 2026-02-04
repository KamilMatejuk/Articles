# https://docs.cloud.google.com/run/docs/tutorials/gpu-gemma-with-ollama

FROM ollama/ollama:latest

ARG PORT_OLLAMA
ENV PORT_OLLAMA=${PORT_OLLAMA}

ARG MODEL_OLLAMA
ENV MODEL_OLLAMA=${MODEL_OLLAMA}

ENV OLLAMA_HOST=0.0.0.0:${PORT_OLLAMA}
ENV OLLAMA_CONTEXT_LENGTH=2048
ENV OLLAMA_DEBUG=false
ENV OLLAMA_KEEP_ALIVE=-1
ENV OLLAMA_NUM_GPU=1
ENV MODEL=${MODEL_OLLAMA}

RUN ollama serve & sleep 5 && ollama pull $MODEL

# preload model into GPU memory on startup
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY entrypoint.sh .
ENTRYPOINT ["bash", "entrypoint.sh"]
