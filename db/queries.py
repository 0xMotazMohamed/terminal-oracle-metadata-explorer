"""
db/queries.py

Every SQL statement of the project.

Naming:  LIST_*  -> gives the names of objects (first menu level)
         others  -> give metadata about ONE selected object

':name' is a bind variable. It is filled with the object the user picked.
We use USER_* views = objects owned by the logged-in user (no extra privileges).
"""

# LISTS 
LIST_TABLES = "SELECT table_name FROM user_tables ORDER BY table_name"
LIST_VIEWS = "SELECT view_name FROM user_views ORDER BY view_name"
LIST_SEQUENCES = "SELECT sequence_name FROM user_sequences ORDER BY sequence_name"
LIST_CONSTRAINTS = "SELECT constraint_name FROM user_constraints ORDER BY constraint_name"
LIST_USERS = "SELECT username FROM all_users ORDER BY username"

#  TABLE metadata 

# USER_TAB_COLUMNS (describes the columns of views).
COLUMNS = """
    SELECT column_id, column_name, data_type, data_length,
           data_precision, data_scale, nullable, data_default
    FROM   user_tab_columns
    WHERE  table_name = :name
    ORDER  BY column_id
"""

TABLE_CONSTRAINTS = """
    SELECT constraint_name, constraint_type, search_condition,
           r_constraint_name, status
    FROM   user_constraints
    WHERE  table_name = :name
    ORDER  BY constraint_type, constraint_name
"""

TABLE_INDEXES = """
    SELECT index_name, index_type, uniqueness, status
    FROM   user_indexes
    WHERE  table_name = :name
    ORDER  BY index_name
"""

TABLE_INDEX_COLUMNS = """
    SELECT index_name, column_position, column_name
    FROM   user_ind_columns
    WHERE  table_name = :name
    ORDER  BY index_name, column_position
"""



#  VIEW metadata 
VIEW_DEFINITION = "SELECT text FROM user_views WHERE view_name = :name"



#  SEQUENCE metadata 
SEQUENCE_PROPERTIES = """
    SELECT sequence_name, min_value, max_value, increment_by,
           cycle_flag, order_flag, cache_size, last_number
    FROM   user_sequences
    WHERE  sequence_name = :name
"""



#  CONSTRAINT metadata 
CONSTRAINT_DETAILS = """
    SELECT constraint_name, constraint_type, table_name, search_condition,
           r_constraint_name, delete_rule, status, validated
    FROM   user_constraints
    WHERE  constraint_name = :name
"""

CONSTRAINT_COLUMNS = """
    SELECT table_name, column_name, position
    FROM   user_cons_columns
    WHERE  constraint_name = :name
    ORDER  BY position
"""



#  USER metadata 
USER_DETAILS = """
    SELECT username, user_id, created
    FROM   all_users
    WHERE  username = :name
"""