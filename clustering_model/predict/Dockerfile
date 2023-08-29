FROM python:3.8.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY clustering_model_predict.py .
COPY ../clustering_model.py .
VOLUME ["/data"]
CMD ["python", "ClusteringModelPredict.py", "--source_file", "/data/source.csv", "--model_path", "/data/model/"]
