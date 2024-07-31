FROM python:3.11.5

COPY ./ /workspace/

WORKDIR /workspace/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/workspace/src:${PYTHONPATH}
