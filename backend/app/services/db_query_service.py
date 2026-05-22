from sqlalchemy import (
    text
)

async def execute_sql(db,sql):

    result = (await db.execute(text(sql)))

    rows = (result.mappings().all())

    return [dict(i)for i in rows]