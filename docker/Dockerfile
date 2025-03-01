FROM python:3.12.7-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src .
# Streamlit Port
EXPOSE 8501
# API PORT
EXPOSE 8005
CMD ["python3", "main.py"]
