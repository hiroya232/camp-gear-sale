FROM python:3.11.5

COPY ./ /workspace/

WORKDIR /workspace/

RUN pip install --no-cache-dir -r requirements.txt

RUN curl -O https://webservices.amazon.com/paapi5/documentation/assets/archives/paapi5-python-sdk-example.zip \
    && unzip paapi5-python-sdk-example.zip \
    && cd paapi5-python-sdk-example \
    && python setup.py install \
    && cd .. \
    && rm -rf paapi5-python-sdk-example.zip paapi5-python-sdk-example

ENV PYTHONPATH=/workspace/src:${PYTHONPATH}
