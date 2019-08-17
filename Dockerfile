# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.5.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ENV DRF_DEBUG_MODE False
ENV DRF_ALLOWED_HOSTS *


# Get the Real World example app
COPY . /drf_src

# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /drf_src

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

VOLUME /drf_src

EXPOSE 8000

ADD start.sh /start.sh
RUN chmod 755 /start.sh

CMD /start.sh
