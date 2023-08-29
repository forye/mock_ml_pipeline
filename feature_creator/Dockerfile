FROM python:3.8.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY feature_creator.py .
VOLUME ["/data"]
CMD ["python", "FeatureCreator.py", "--ftrs_model", "/data/features_creator_models/feature_creator.pkl", "--source_files", "/data/chunker/", "--ftrs_path", "/data/ftr_data/", "--res_filename", "features.csv"]
