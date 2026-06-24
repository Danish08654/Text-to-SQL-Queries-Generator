def validate_sql(query: str):

    q = query.lower().strip()

    blocked = [
        "drop", "delete", "update", "insert",
        "alter", "truncate", "create", "attach"
    ]

    for b in blocked:
        if b in q:
            return False, f"Blocked unsafe operation: {b}"

    if not q.startswith("select"):
        return False, "Only SELECT queries allowed"

    return True, "SQL is safe"