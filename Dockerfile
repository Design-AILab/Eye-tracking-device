FROM python:3.6-alpine3.10

# for numpy
## RUN apk update
## RUN apk add make automake gcc g++ subversion python3-dev

# https://stackoverflow.com/questions/57787424/django-docker-python-unable-to-install-pillow-on-python-alpine
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps \
    && apk add make automake gcc g++ subversion python3-dev  \
    && apt-get install -y openssl

COPY requirement.txt .
# Copy the current directory contents into the container at /app
ADD . /app

# Set the working directory to /app
WORKDIR /app

# create certificate
COPY generate-certificate.sh /cert/generate-certificate.sh

CMD [ "/cert/generate-certificate.sh" ]


# this is for matplotlib
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# Make port 5000 available to the world outside this container
# Expose 443 for https
EXPOSE 443

# Run app.py when the container launches
CMD ["python", "run.py"]
