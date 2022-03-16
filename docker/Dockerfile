FROM python:3.9-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN python EmployeeManager/manage.py collectstatic

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD [ "./EmployeeManager/build_and_run.sh" ]
