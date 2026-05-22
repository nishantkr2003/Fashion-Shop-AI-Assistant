import re


def validate_sql(
    sql
):

    sql = sql.strip()

    if "```" in sql:

        sql = (

            sql

            .replace(
                "```sql",
                ""
            )

            .replace(
                "```",
                ""
            )

        )

    sql = sql.strip()

    if not sql.lower().startswith(
        "select"
    ):

        raise Exception(
            "Only SELECT allowed"
        )

    blocked = [

        r"\bdrop\b",
        r"\bdelete\b",
        r"\binsert\b",
        r"\bupdate\b",
        r"\btruncate\b",
        r"\balter\b"

    ]

    for p in blocked:
        if re.search(p,sql.lower()):
            raise Exception("Unsafe SQL")

    return sql