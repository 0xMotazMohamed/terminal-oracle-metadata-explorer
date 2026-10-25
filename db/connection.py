"""
db/connection.py

ONLY file that talks to Oracle directly.
Have two jobs:
  1. connect()   -> open a connection with the user's credentials
  2. run_query() -> run one SELECT and give back (column_names, rows)
"""

import oracledb

import config


def build_dsn(service_name):
    """
    Turn what the user typed into a connection string (DSN).

    - If the user typed only 'orcl'              -> we build localhost:1521/orcl
    - If the user typed a full 'host:port/name'  -> we use it exactly as typed
    """
    if ":" in service_name or "/" in service_name:
        return service_name
    return oracledb.makedsn(
        config.DEFAULT_HOST, config.DEFAULT_PORT, service_name=service_name
    )


def connect(username, password, service_name):
    """Open and return a connection. Raises oracledb.DatabaseError on failure."""
    return oracledb.connect(
        user=username,
        password=password,
        dsn=build_dsn(service_name),
    )


def run_query(connection, sql, params=None):
    """
    Run a SELECT statement and return (columns, rows).

    - columns : list of column names, e.g. ['COLUMN_NAME', 'DATA_TYPE']
    - rows    : list of tuples, one tuple per row
    - params  : dict of bind variables, e.g. {'name': 'EMPLOYEES'}
                (bind variables are safe: user input is never glued into SQL)
    """
    with connection.cursor() as cursor: # cursor, (the object that sends SQL and reads results).
        cursor.execute(sql, params or {}) # params is a dict like {"name": "EMPLOYEES"} that fills the :name placeholder.
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchmany(config.MAX_ROWS)
    return columns, rows