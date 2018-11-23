FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
COPY ./app/Python-Snake/Python-Snake ./app

CMD [ "python", "./app/main.py" ]