FROM python:3.7.9
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
CMD [ "python", "chatbot.py" ]