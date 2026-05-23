import pandas as pd
from sqlalchemy import text
from app.db import engine


def import_csv(path, table):

    df = pd.read_csv(path)

    df.columns = [
        c.strip().lower()
        for c in df.columns
    ]

    inserted = 0
    skipped = 0
    failed = 0

    with engine.begin() as conn:

        db_cols = conn.execute(
            text(
                f"""
                SELECT *
                FROM {table}
                LIMIT 1
                """
            )
        ).keys()

        allowed = [
            c
            for c in df.columns
            if c in db_cols
        ]

        for row in (
            df.to_dict("records")
        ):

            try:

                data = {
                    k: row[k]
                    for k in allowed
                }

                duplicate = False

                if "name" in data:

                    duplicate = conn.execute(
                        text(
                            f"""
                            SELECT 1
                            FROM {table}
                            WHERE name=:name
                            LIMIT 1
                            """
                        ),
                        {
                            "name":
                            data["name"]
                        }
                    ).first()

                if duplicate:

                    skipped += 1
                    continue

                cols = ",".join(
                    allowed
                )

                vals = ",".join(
                    [
                        f":{x}"
                        for x in allowed
                    ]
                )

                conn.execute(
                    text(
                        f"""
                        INSERT INTO
                        {table}
                        ({cols})

                        VALUES
                        ({vals})
                        """
                    ),
                    data
                )

                inserted += 1

            except Exception:
                failed += 1

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "columns": allowed,
        "total": len(df)
    }