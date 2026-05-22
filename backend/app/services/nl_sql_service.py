import re
from pathlib import Path
from app.services.ollama_service import (generate)

async def generate_sql(question):
    prompt = (Path("app/prompts/sql_prompt.txt").read_text(encoding="utf-8"))

    prompt = (prompt.replace("{question}",question))

    sql = (await generate(prompt))

    sql = re.sub(r"```sql|```","",sql)
    sql = sql.strip()
    if ";" in sql:
        sql = (sql.split(";")[0])
    print("\nFINAL SQL:\n",sql)

    return sql