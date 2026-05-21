# import asyncio

# from sqlalchemy import text

# from app.db.database import engine


# async def fix():

#     async with engine.begin() as conn:

#         await conn.execute(
#             text(
#                 """
# UPDATE alembic_version
# SET version_num='b1c229fede24'
# """
#             )
#         )

#     print("fixed")


# asyncio.run(fix())

from sqlalchemy import text
from app.db.database import AsyncSessionLocal
import asyncio


async def check():

    async with AsyncSessionLocal() as db:

        r = await db.execute(
            text(
                """
SELECT tablename
FROM pg_tables
WHERE tablename='products'
"""
            )
        )

        print(r.scalar())


asyncio.run(check())