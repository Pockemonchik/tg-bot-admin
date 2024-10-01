# 
FROM python:3.12

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy entrypoint.sh
COPY ./docker/entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod 777 /usr/src/app/entrypoint.sh

COPY ../pyproject.toml ./
# install dependencies
RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry\
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# copy project
COPY . .
ENV PYTHONPATH /usr/src/app/src
ENTRYPOINT ["sh", "entrypoint.sh"]
# 