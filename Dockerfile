FROM python:3.12-slim

MAINTAINER Sombra Team(https://github.com/Sombra-MLET2)

WORKDIR /opt/app/

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY src ./src

EXPOSE 80
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]