"""
config.py

All the "settings" of the project live here
"""

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8521


DEFAULT_SERVICE = "orcl" # Suggested service name 


MAX_ROWS = 500 # Safety limit (no more than this rows in one result)


MAX_CELL_WIDTH = 40 # Long values (like a constraint condition) are cut to this width in tables


MAX_LOGIN_ATTEMPTS = 3 
