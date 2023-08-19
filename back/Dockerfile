FROM python:3.9

RUN apt-get update && \
    apt-get install -y libpq-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "run_back.py"]
