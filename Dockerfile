FROM python:3.10

WORKDIR /app
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 freeze > requirements.txt
RUN pip3 install -U aiogram
RUN	pip3 install -U pyowm
RUN	pip3 install -U googletrans==3.1.0a0
RUN	pip3 install -U youtube-search


ENTRYPOINT ["python3", "main.py"]   