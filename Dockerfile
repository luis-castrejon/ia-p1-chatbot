FROM python:3.7.9

# Establecer la zona horaria en el Dockerfile
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY . /app

CMD [ "python", "chatbot.py" ]