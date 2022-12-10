FROM python:3.6
ADD ./app/ /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py

# docker build -t web .
