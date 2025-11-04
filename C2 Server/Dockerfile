FROM python:3.10-slim

WORKDIR /app

COPY . /app/
RUN pip install --no-cache-dir -r Requirements.txt

EXPOSE 8880
CMD ["python", "app.py"]
