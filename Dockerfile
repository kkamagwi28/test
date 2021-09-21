FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./ /code/
COPY /home/jellyfish/.ssh/id_rsa.pub /.ssh/id_rsa.pub

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]