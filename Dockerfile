FROM python:3.12-slim
WORKDIR /opt/app/

COPY requirements.txt ./requirements.txt
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 80
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]