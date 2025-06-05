FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pybabel compile -d translations
EXPOSE 5000
CMD ["python", "run.py"]
