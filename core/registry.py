"""
core/registry.py

It describes every object type as DATA:
  - its name in the menu
  - the query that lists its objects
  - the metadata options available once an object is selected
"""

from dataclasses import dataclass, field
from typing import List

from db import queries


@dataclass # We use it because this class only HOLDS data (no behavior).
class MetadataOption:
    """One choice in the 'Choose what to view' menu."""
    label: str              # text shown in the menu, e.g. "Columns"
    sql: str                # query that uses the :name bind variable
    as_text: bool = False   # True = print as plain text (e.g. a view's SQL)


@dataclass
class ObjectType:
    """One choice in the main menu, e.g. 'Tables'."""
    name: str                                   # text shown in the main menu
    list_sql: str                               # query returning object names
    options: List[MetadataOption] = field(default_factory=list)


# The order here is the order of the main menu.
OBJECT_TYPES = [
    ObjectType(
        name="Tables",
        list_sql=queries.LIST_TABLES,
        options=[
            MetadataOption("Columns", queries.COLUMNS),
            MetadataOption("Constraints", queries.TABLE_CONSTRAINTS),
            MetadataOption("Indexes", queries.TABLE_INDEXES),
            MetadataOption("Index columns", queries.TABLE_INDEX_COLUMNS),
        ],
    ),
    ObjectType(
        name="Views",
        list_sql=queries.LIST_VIEWS,
        options=[
            MetadataOption("Columns", queries.COLUMNS),
            MetadataOption("Definition (SQL text)", queries.VIEW_DEFINITION, as_text=True),
        ],
    ),
    ObjectType(
        name="Sequences",
        list_sql=queries.LIST_SEQUENCES,
        options=[
            MetadataOption("Properties", queries.SEQUENCE_PROPERTIES),
        ],
    ),
    ObjectType(
        name="Constraints",
        list_sql=queries.LIST_CONSTRAINTS,
        options=[
            MetadataOption("Details", queries.CONSTRAINT_DETAILS),
            MetadataOption("Columns", queries.CONSTRAINT_COLUMNS),
        ],
    ),
    ObjectType(
        name="Users",
        list_sql=queries.LIST_USERS,
        options=[
            MetadataOption("Details", queries.USER_DETAILS),
        ],
    ),
]