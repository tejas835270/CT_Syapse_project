FROM python:3.7

LABEL team="qa" \
      service="qa-automation-drt-haw"

ENV PATH=$PATH:/home/user/.local/bin \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIP_NO_CACHE_DIR=off \
    PIP_USER=1 \
# This env var is set to true to pass on to driver so that it knows it is running from docker
    IS_DOCKER=true

# Run as non root user (best practice)
ARG ENVIRONMENT
ENV WORKDIR=/srv
ENV TESTS="$WORKDIR/qa_automation_drt_haw"
RUN mkdir -p "$TESTS"

# Avoid mixing $HOME and WORKDIR so important persistent files in $HOME such as
# ~/.local don't conflict with service runtime files.
WORKDIR $WORKDIR
ARG PACKAGECLOUD_TOKEN

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
# This install chrome in docker
RUN apt-get install -y google-chrome-stable


# install chromedriver
RUN apt-get install -yqq unzip

# This fetches the correct version of chromedriver
#RUN wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip"
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod 777 /usr/local/bin/chromedriver
RUN chmod 777 /usr/bin/google-chrome

# set display port to avoid crash
ENV DISPLAY=:99

# Run as a non-root user.
RUN useradd -ms /bin/bash user \
    && mkdir -p /srv/qa_reports \
    && chown -R user:user /srv
USER user

# Install pipenv.
# Workaround https://github.com/pypa/pipenv/issues/3222 use old version.
RUN python -m pip install --upgrade --user pipenv==v2018.10.9

# Copy required project files into the WORKDIR.
COPY --chown=user:user Pipfile* setup.py setup.cfg $WORKDIR/

# Install environment dependencies with Pipenv. If no lockfile is present, we skip it.
RUN test -f "./Pipfile.lock" && pipenv install --system --keep-outdated --ignore-pipfile || pipenv install --system --skip-lock

# Copy the project directory (https://github.com/moby/moby/issues/29211)
COPY qa_automation_drt_haw $TESTS

# Copy the entrypoint files for booting the application.
COPY --chown=user:user runner /usr/local/bin/

VOLUME /srv/qa_reports
# Set the command executed first when the container run
ENTRYPOINT ["runner"]
