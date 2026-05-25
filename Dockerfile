# Stage 1: Build aw-webui (Vue.js)
FROM node:18-alpine AS frontend-build
WORKDIR /app/aw-webui
COPY aw-webui/package*.json ./
RUN npm install
COPY aw-webui/ ./
RUN npm run build

# Stage 2: Python Runtime for aw-server
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies if required (e.g., for building native extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy aw-core and install it
COPY aw-core/ /app/aw-core/
RUN pip install -e /app/aw-core/

# Copy aw-server and install its dependencies
COPY aw-server/ /app/aw-server/
WORKDIR /app/aw-server
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Copy the built Vue frontend into aw-server's static directory
COPY --from=frontend-build /app/aw-webui/dist /app/aw-server/aw_server/static

# Setup Environment variables
ENV PORT=5700
ENV HOST=0.0.0.0
ENV AW_DATA_DIR=/app/data/pss-tracker
ENV AW_LOG_DIR=/app/logs

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5700/health || exit 1

EXPOSE 5700
CMD ["python", "-m", "aw_server", "--port", "5700", "--host", "0.0.0.0"]
