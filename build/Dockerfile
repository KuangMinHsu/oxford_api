FROM python:3.9-slim

WORKDIR /usr/src/app
#RUN apt update && apt install python3-protobuf python3-distutils
#COPY bin/mysql-connector-python-py3_8.0.27-1debian11_amd64.deb .
#RUN dpkg -i mysql-connector-python-py3_8.0.27-1debian11_amd64.deb
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /var/log/oxford-api/

CMD ["tail", "-f", "/etc/os-release"]
#CMD [ "python", "./your-daemon-or-script.py" ]
