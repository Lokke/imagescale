FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create static directory if it doesn't exist
RUN mkdir -p static

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8724

# Start with Gunicorn production server
CMD ["gunicorn", "--bind", "0.0.0.0:8724", "--workers", "4", "--timeout", "60", "backend.app:app"]
