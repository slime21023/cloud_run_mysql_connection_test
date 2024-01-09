from litestar import Litestar, get
import os
import sqlalchemy
import logging

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_host = os.environ[
        "INSTANCE_HOST"
    ]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    db_port = os.environ["DB_PORT"]  # e.g. 3306

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
        # ...
    )

    logging.info("Database connected!")
    return pool


pool = None


@get("/")
async def hello_world() -> str:
    return "Hello, world!"


@get("/health_check")
async def health_check() -> bool:
    return True


@get("/is_connected")
async def is_connected() -> bool:
    if pool is None:
        return False

    res = pool.execute("select 1=1;").first()
    if res is not None:
        return True
    else:
        return False

pool = connect_tcp_socket()
app = Litestar([hello_world, is_connected])
