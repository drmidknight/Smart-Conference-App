FROM python:3.10

WORKDIR /app

COPY . /app

COPY ./app/requirements.txt /app

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r /app/requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "http://dev-1.aiti-kace.com.gh", "--port", "8000"]