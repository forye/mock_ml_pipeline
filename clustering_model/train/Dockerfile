FROM python:3.8.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY clustering_model_train.py .
COPY ../clustering_model.py .
VOLUME ["/data"]
CMD ["python", "clustering_model_train.py", "--source_file", "/data/source.csv", "--model_filename_and_path", "/data/models/clustering_model.pkl"]
