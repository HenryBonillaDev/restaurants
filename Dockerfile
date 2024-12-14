FROM python:latest

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]