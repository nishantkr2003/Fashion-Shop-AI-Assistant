import sys
from pathlib import Path

ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.append(
    str(ROOT)
)

import asyncio
import pandas as pd

from app.db.database import (
    AsyncSessionLocal
)

from app.models.product import (
    Product
)


CSV = (
    ROOT.parent
    /
    "Data"
    /
    "products"
    /
    "products.csv"
)


async def run():

    async with AsyncSessionLocal() as db:

        df = pd.read_csv(
            CSV
        )

        for row in (

            df.to_dict(
                "records"
            )

        ):

            db.add(

                Product(
                    **row
                )

            )

        await db.commit()

        print(

            f"{len(df)} products imported"

        )


asyncio.run(
    run()
)