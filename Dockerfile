FROM python:3.6
WORKDIR /app
COPY base /app/base	
COPY bin /app/bin
COPY templates /app/templates
COPY config.py requirements.txt ResthttpckEx.py setup.py /app/
RUN pip install -r requirements.txt
RUN python setup.py develop
RUN mkdir -p /var/log/resthttpck/cdraccess/ /etc/resthttpck/
