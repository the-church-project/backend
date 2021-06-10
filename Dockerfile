FROM python:3.9.5

# RUN apt-get update && apt-get install -y \
#    apt-file \
#    wget \
#    curl \
#    git \
#    python3-virtualenv
# RUN apt-file update
RUN apt-get update && apt-get install -y

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV

WORKDIR /backend
COPY requirements.txt .

RUN pip install wheel && pip install -r requirements.txt

# COPY server .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--verbosity=3"]
# CMD ["ls"]
