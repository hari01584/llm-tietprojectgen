FROM texlive/texlive:latest

# install python
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /usr/src/app

# dont write pyc files
# dont buffer to stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

# dependencies
RUN pip install --break-system-packages --upgrade pip setuptools wheel \
    && pip install --break-system-packages -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./ /app