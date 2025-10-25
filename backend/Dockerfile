FROM python:3.11-slim

WORKDIR /app

# Copy project
COPY . /app

# Install minimal deps; if you have a requirements.txt prefer that (pip install -r requirements.txt)
RUN pip install --no-cache-dir flask gunicorn pymysql

EXPOSE 5000

# Use gunicorn to serve the Flask app (app:create_app() uses the factory in app.py)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]
