# ==============================
FROM registry.access.redhat.com/ubi9/python-312 AS appbase
# ==============================

# Branch or tag used to pull python-uwsgi-common.
ARG UWSGI_COMMON_REF=main

USER root
WORKDIR /app

RUN mkdir /entrypoint

# chmod=755 = rwxr-xr-x i.e. owner can read, write and execute, group and others can read and execute.
#
# Related to SonarCloud security hotspot docker:S6470 i.e.
# "Recursively copying context directories is security-sensitive" i.e.
# https://rules.sonarsource.com/docker/RSPEC-6470/
# see .dockerignore for info on what is not copied here:
COPY --chown=root:root --chmod=755 . /app/

RUN dnf update -y  \
    && dnf install -y nmap-ncat  \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && uwsgi --build-plugin https://github.com/City-of-Helsinki/uwsgi-sentry \
    && dnf clean all

# Build and copy specific python-uwsgi-common files.
ADD https://github.com/City-of-Helsinki/python-uwsgi-common/archive/${UWSGI_COMMON_REF}.tar.gz /usr/src/
RUN mkdir -p /usr/src/python-uwsgi-common && \
    tar --strip-components=1 -xzf /usr/src/${UWSGI_COMMON_REF}.tar.gz -C /usr/src/python-uwsgi-common && \
    cp /usr/src/python-uwsgi-common/uwsgi-base.ini /app && \
    uwsgi --build-plugin /usr/src/python-uwsgi-common && \
    rm -rf /usr/src/${UWSGI_COMMON_REF}.tar.gz && \
    rm -rf /usr/src/python-uwsgi-common

COPY --chown=root:root --chmod=755 docker-entrypoint.sh /entrypoint/docker-entrypoint.sh
ENTRYPOINT ["/entrypoint/docker-entrypoint.sh"]

# ==============================
FROM appbase AS development
# ==============================

RUN pip install --no-cache-dir -r /app/requirements-dev.txt

ENV DEV_SERVER=1

USER default
EXPOSE 8081/tcp

# ==============================
FROM appbase AS production
# ==============================

RUN SECRET_KEY="only-used-for-collectstatic" python manage.py collectstatic

USER default
EXPOSE 8000/tcp
