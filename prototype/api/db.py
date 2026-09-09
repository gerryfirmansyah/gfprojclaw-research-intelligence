import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


ENV_FILE = "/opt/gfprojclaw/config/runtime.env"

load_dotenv(ENV_FILE)


def get_dsn() -> str:
    host = os.environ["GFPROJ_DB_HOST"]
    port = os.environ["GFPROJ_DB_PORT"]
    dbname = os.environ["GFPROJ_DB_NAME"]
    user = os.environ["GFPROJ_DB_USER"]
    password = os.environ["GFPROJ_DB_PASSWORD"]

    return (
        f"host={host} "
        f"port={port} "
        f"dbname={dbname} "
        f"user={user} "
        f"password={password}"
    )


@contextmanager
def db():
    conn = psycopg.connect(
        get_dsn(),
        row_factory=dict_row,
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
