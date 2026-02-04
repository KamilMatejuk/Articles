# https://google.github.io/adk-docs/deploy/cloud-run/#code-files

FROM python:3.14-slim

ARG PORT_ADK
ENV PORT_ADK=${PORT_ADK}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# patch Google search tool is not supported for non-Gemini models
RUN sed -i '71a\    return llm_request.config.tools.append(types.Tool(google_search=types.GoogleSearch()))' \
    /usr/local/lib/python3.14/site-packages/google/adk/tools/google_search_tool.py

RUN adduser --disabled-password --gecos "" myuser && chown -R myuser:myuser /app

COPY *.py .
COPY agent/ ./agent/

USER myuser

ENV PATH="/home/myuser/.local/bin:$PATH"

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT_ADK"]
