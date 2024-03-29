FROM python:3.9-alpine 

# install PDM
RUN pip install -U pip
RUN pip install pdm litestar[standard]

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN pdm export -o requirements.txt --without-hashes --prod && pip install -r requirements.txt

CMD ["sh", "-c", "litestar --app src.cloud_run_mysql_connection_test:app run --host 0.0.0.0 --wc 2"]

