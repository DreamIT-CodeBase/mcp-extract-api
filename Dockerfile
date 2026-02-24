FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port for FastMCP/HTTP
EXPOSE 8050
EXPOSE 3001  
# MCP transport port

# Run your server when container starts
CMD ["sh", "-c", "python server.py & uvicorn api:app --host 0.0.0.0 --port 8050"]