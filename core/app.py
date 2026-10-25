"""
core/app.py
-----------
The FLOW of the program. It connects the other layers but contains
no SQL text and no print-formatting logic.

The flow is three nested loops (each has a "Back" option):

    login
      └─ main_menu_loop      choose an object TYPE      (Exit ends the app)
           └─ browse_objects     choose one OBJECT      (Back -> main menu)
                └─ explore_object    choose what to VIEW (Back -> object list)
"""

import oracledb

import config
from core.registry import OBJECT_TYPES
from db import connection
from ui import display, menus, prompts


#  helpers 
def safe_query(conn, sql, params=None):
    """
    Run a query, but never crash the app if Oracle complains
    (missing privilege, dropped object, lost connection...).
    Returns (columns, rows) or None if an error happened.
    """
    try:
        return connection.run_query(conn, sql, params)
    except oracledb.DatabaseError as error:
        print(f"\nDatabase error: {error}")
        return None


def fetch_names(conn, object_type):
    """Return the list of object names for a type, e.g. ['EMPLOYEES', ...]."""
    result = safe_query(conn, object_type.list_sql)
    if result is None:
        return []
    _columns, rows = result
    return [row[0] for row in rows]


#  steps 
def login():
    """Ask for credentials until the connection works (or attempts run out)."""
    for attempt in range(1, config.MAX_LOGIN_ATTEMPTS + 1):
        username = prompts.ask_text("Enter username")
        password = prompts.ask_password("Enter password")
        service = prompts.ask_text("Enter service name", default=config.DEFAULT_SERVICE)

        try:
            conn = connection.connect(username, password, service)
            print(f"\nConnected as {username.upper()}.")
            return conn
        except oracledb.DatabaseError as error:
            print(f"\nConnection failed: {error}")
            print(f"Attempt {attempt} of {config.MAX_LOGIN_ATTEMPTS}.\n")
    return None


def explore_object(conn, object_type, object_name):
    """Level 3: let the user view metadata of ONE object, until they go back."""
    while True:
        labels = [option.label for option in object_type.options]
        choice = menus.show_menu(
            f"Choose what to view about {object_name}:", labels, "Back"
        )
        if choice is None:
            return

        option = object_type.options[choice]
        result = safe_query(conn, option.sql, {"name": object_name})
        if result is None:
            continue

        columns, rows = result
        print(f"\n=== {option.label} of {object_name} ===")
        if option.as_text:
            display.print_text(rows)
        else:
            display.print_table(columns, rows)


def browse_objects(conn, object_type):
    """Level 2: list the objects of one type and let the user pick one."""
    while True:
        names = fetch_names(conn, object_type)
        if not names:
            print(f"\nNo {object_type.name.lower()} found.")
            return

        choice = menus.show_menu(
            f"Available {object_type.name}:", names, "Back to main menu"
        )
        if choice is None:
            return

        selected = names[choice]
        print(f"\nYou selected: {selected}")
        explore_object(conn, object_type, selected)


def main_menu_loop(conn):
    """Level 1: choose an object type. Runs until the user picks Exit."""
    while True:
        labels = [object_type.name for object_type in OBJECT_TYPES]
        choice = menus.show_menu(
            "Select the object type you want to view:", labels, "Exit"
        )
        if choice is None:
            return
        browse_objects(conn, OBJECT_TYPES[choice])


#  entry point 
def run():
    """Start the whole application."""
    print("Welcome to Oracle Metadata Explorer!")
    print("-----------------------------------")

    conn = login()
    if conn is None:
        print("Could not connect. Goodbye!")
        return

    try:
        main_menu_loop(conn)
    finally:
        conn.close()          # always release the connection
    print("\nConnection closed. Goodbye!")