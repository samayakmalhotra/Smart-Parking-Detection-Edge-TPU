FROM debian:latest
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install python3 python3-pip && \
    apt-get install gnupg && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    apt-get update
    apt-get install python3-edgetpu
RUN mkdir /app
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile
COPY . /app
