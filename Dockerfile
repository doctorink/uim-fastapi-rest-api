FROM python:3.9
# Adding the requirements to the container
ADD requirements.txt /
# Copy app content
ADD app /app
# Copy your models
ADD models /models
# Change to / as working dir
WORKDIR /
# Update container software
RUN apt-get update
RUN set -ex && apt-get install -y apt-transport-https
RUN set -ex \
    && apt-get install --yes --allow-unauthenticated \
         apt-utils \
         g++ \
         gcc \
         git

# Install Python requirements
RUN python -m venv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r /requirements.txt"

# Create unprivileged user
RUN adduser --disabled-password --gecos '' demo
RUN chown -R demo app
RUN chmod a+wx /var/run

# Remember to configure the reverse proxy or deployment enviroment to use this port
ENV PORT=8080
EXPOSE $PORT

# Start the HTTP server
CMD /venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT