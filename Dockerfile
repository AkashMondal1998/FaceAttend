FROM python:3.10-bullseye

RUN apt update && apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

COPY . /attendance_api

WORKDIR /attendance_api

RUN chmod +x wait-for-it.sh

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["./wait-for-it.sh", "-t", "30", "localhost:3307", "--", "python", "app.py"]


