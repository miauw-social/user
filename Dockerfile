FROM python:alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install requirements.txt
COPY . .
CMD ["python", "main.py"]