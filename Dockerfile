FROM python:3

LABEL maintainer="ConvAI"

WORKDIR /Query_Answering

COPY . /Query_Answering

RUN pip install --no-cache-dir --user -r requirements.txt

CMD ["python", "./query_answering_api.py"]
