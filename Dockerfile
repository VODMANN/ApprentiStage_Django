FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN echo "python manage.py migrate" > init.sh \
    && echo "python manage.py runserver 0.0.0.0:8000" >> init.sh \
    && chmod +x init.sh

EXPOSE 8000

CMD ["/bin/bash", "init.sh"]
