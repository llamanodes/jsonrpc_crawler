# copy everything into a single image
FROM python:3.11

# set up ENV. do this first because it won't ever change
ENV PATH /llama/venv/bin:$PATH

# Create llama user to avoid running container with root
RUN set -eux; \
    \
    mkdir /llama; \
    adduser --home /llama --shell /sbin/nologin --gecos '' --no-create-home --disabled-password --uid 1000 llama; \
    chown -R llama /llama

# Run everything else as the "llama" user, not root
USER llama
# ENV HOME /llama  # TODO: do we need this?
WORKDIR /llama

# create virtualenv
RUN --mount=type=cache,target=/llama/.cache \
    \
    python3 -m venv /llama/venv

# install app dependencies
RUN --mount=type=bind,source=requirements.txt,target=/llama/venv/requirements.txt \
    --mount=type=cache,target=/llama/.cache \
    \
    pip install -r /llama/venv/requirements.txt

# install app
COPY ./entrypoint.py /llama/venv/bin/

ENTRYPOINT ["entrypoint.py"]
