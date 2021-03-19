FROM python:3.6-buster
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install libpq-dev -y tzdata && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
      apt-get install \
      --virtual=.build-dependencies \
      gcc \
      musl-dev \
      git \
      python3-dev \
      jpeg-dev \
      # Pillow
      zlib-dev \
      libffi-dev \
      freetype-dev \
      lcms2-dev \
      openjpeg-dev \
      tiff-dev \
      tk-dev \
      tcl-dev \
      harfbuzz-dev \
      fribidi-dev && \
    python -m pip --no-cache install -U pip && \
    python -m pip --no-cache --use-feature=2020-resolver install -r requirements/production.txt && \
    # apt-get del --purge .build-dependencies

EXPOSE 8000
