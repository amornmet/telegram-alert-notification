FROM python:3.6
ADD ./app/ /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
