"""
SQL guard utilities.

This module provides a very simple check for potentially destructive
SQL statements.  It is intended as a last‑line guard before executing
dynamically generated SQL.  The heuristics are rudimentary and should
not be considered sufficient for production use; you may wish to
integrate a proper parser or parameterised queries.
"""

import re
from typing import Iterable

_DANGEROUS_KEYWORDS: Iterable[str] = {
    "drop",
    "delete",
    "truncate",
    "alter",
    "update",
    "insert",
    "--",  # SQL comment injection
}


def is_safe_sql(query: str) -> bool:
    """Return ``True`` if the query string does not contain dangerous keywords.

    The check is case‑insensitive and looks for whole words.  It does not
    guarantee safety but catches some obvious attempts at destructive
    commands or comment injection.

    Args:
        query: The SQL string to inspect.

    Returns:
        True if none of the blacklisted keywords appear in the query.
    """

    lowered = query.lower()
    for word in _DANGEROUS_KEYWORDS:
        pattern = rf"\b{re.escape(word)}\b"
        if re.search(pattern, lowered):
            return False
    return True


def guard_query(query: str) -> None:
    """Raise ``ValueError`` if the provided SQL query appears dangerous.

    Args:
        query: SQL query to validate.

    Raises:
        ValueError: If ``query`` contains any of the dangerous keywords.
    """

    if not is_safe_sql(query):
        raise ValueError("Potentially destructive SQL detected; execution aborted.")