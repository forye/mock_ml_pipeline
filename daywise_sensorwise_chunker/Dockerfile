FROM python:3.8.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY daywise_sensorwise_chunker.py .
VOLUME ["/data"]
CMD ["python", "DaywiseSensorwiseChunker.py", "--source_file", "/data/source_data/", "--destination_path", "/data/chunker/"]
