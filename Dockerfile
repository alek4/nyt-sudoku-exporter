FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py fetch_nyt.py append_to_opensudoku.py ./

CMD ["python", "main.py"]