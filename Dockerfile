FROM python:3.11.5

WORKDIR /workspace/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
