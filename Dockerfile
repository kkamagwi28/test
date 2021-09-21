FROM python:3
ENV PYTHONUNBUFFERED=1

#ADD /home/jellyfish/.ssh/id_rsa.pub:/usr/local/share/.ssh/id_rsa.pub
#RUN chmod 644 /usr/local/share/.ssh/id_rsa.pub

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./ /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]