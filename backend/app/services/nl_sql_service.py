from pathlib import Path


async def generate_sql(question: str):
    q = question.lower()
    sql = """
SELECT *
FROM products
WHERE 1=1
"""

    if "shoes" in q:
        sql += (" AND category='Shoes'")

    if "black" in q:
        sql += (" AND color ILIKE '%Black%'")

    if "nike" in q:

        sql += (" AND brand='Nike'")

    if "under" in q:
        words = q.split()
        for i in range(len(words)):
            if words[i] == "under":
                sql += (f"""AND price<={words[i+1]}""")

    sql += (" LIMIT 10")

    return sql