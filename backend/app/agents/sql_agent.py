from app.services.nl_sql_service import (
    generate_sql
)

from app.services.db_query_service import (
    execute_sql
)

from app.services.sql_guard import (
    validate_sql
)


async def search_products(db,question):

    sql = (await generate_sql(question))

    sql = validate_sql(sql)
    print("\nSQL:\n",sql)

    return (await execute_sql(db,sql))