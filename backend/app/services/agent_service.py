# from app.agents.router_agent import (
#     route
# )

# from app.agents.sql_agent import (
#     search_products
# )

# from app.agents.memory_agent import (
#     build_context
# )

# from app.services.memory_service import (
#     load_memory
# )


# async def run_agent(
# db,
# conversation_id,
# message
# ):

#     history = await load_memory(db,conversation_id)
#     context = build_context(history,message)
#     selected = route(context)

#     if selected == "sql":
#         products = (
#             search_products(context)
#         )
#         if not products:
#             return ("No products found")

#         result = []
#         for p in products[:5]:
#             result.append(f"""{p["name"]}Brand: {p["brand"]}Price: ${p["price"]}""")
#         return "\n".join(result)
#     return ("General response")















# from app.agents.router_agent import route
# from app.agents.sql_agent import search_products

# from app.services.memory_service import (
#     load_memory
# )

# import re


# def extract_filters(history):

#     brand = None
#     price = None

#     text = " ".join(
#         [
#             str(m.content).lower()
#             for m in history
#         ]
#     )

#     brands = [
#         "nike",
#         "adidas",
#         "vans",
#         "converse",
#         "new balance",
#         "asics",
#     ]

#     # Detect latest matching brand
#     for b in brands:
#         if b in text:
#             brand = b

#     # Extract price patterns:
#     # "under 100"
#     # "below 50"
#     match = re.search(
#         r"(under|below)\s+(\d+)",
#         text
#     )

#     if match:
#         price = float(match.group(2))

#     return brand, price


# async def run_agent(
#     db,
#     conversation_id,
#     message
# ):

#     # -----------------------------
#     # Load memory/history
#     # -----------------------------

#     history = await load_memory(
#         db,
#         conversation_id
#     )

#     # -----------------------------
#     # Route request
#     # -----------------------------

#     selected = route(message)

#     if selected != "sql":
#         return "General response"

#     # -----------------------------
#     # Search products
#     # -----------------------------

#     products = search_products(
#         message
#     )

#     # -----------------------------
#     # Extract contextual filters
#     # -----------------------------

#     brand, price = extract_filters(
#         history
#     )

#     # -----------------------------
#     # Apply brand filter
#     # -----------------------------

#     if brand:

#         products = [
#             p
#             for p in products
#             if brand.lower()
#             in p["brand"].lower()
#         ]

#     # -----------------------------
#     # Apply price filter
#     # -----------------------------

#     if price is not None:

#         products = [
#             p
#             for p in products
#             if float(p["price"]) <= price
#         ]

#     # -----------------------------
#     # No results
#     # -----------------------------

#     if not products:
#         return "No matching products found."

#     # -----------------------------
#     # Format response
#     # -----------------------------

#     result = []

#     for i, p in enumerate(
#         products[:5],
#         start=1
#     ):

#         result.append(
#             f"""
# {i}. {p['name']}

# Brand: {p['brand']}
# Price: ${p['price']}
# Rating: {p['rating']}
# Stock: {p['stock']}
# """
#         )

#     return "\n".join(result)










from multiprocessing import context

from app.agents.router_agent import route

from app.agents.sql_agent import (
    search_products
)

from app.agents.memory_agent import (
    extract_memory
)

from app.services.memory_service import (
    load_memory
)

from app.services.context_service import (
    build_query
)

async def run_agent(
    db,
    conversation_id,
    message
):

    history = (
        await load_memory(
            db,
            conversation_id
        )
    )

    memory = (extract_memory(history,message))

    context = " ".join(
    [
        str(v)
        for v in memory.values()
        if v
    ]

)

    selected = route(context + " " + message)

    if selected != "sql":
        return ("General response")

    query = []

    for k, v in memory.items():
        if v:
            query.append(str(v))

    # products = await search_products(db," ".join(query))
    q = build_query(conversation_id," ".join(query))

    print("\nFINAL QUERY:",q)
    products = await search_products(db,q)

    if memory["brand"]:

        products = [
            p
            for p in products
            if (memory["brand"] in p["brand"].lower())
        ]

    if memory["max_price"]:
        products = [
            p
            for p in products
            if (float(p["price"]) <= memory["max_price"])
        ]
    if not products:
        return ("No products found.")
    result = []
    for i, p in enumerate(products[:5],1):
        result.append(

f"""
{i}. {p["name"]}

Brand:
{p["brand"]}

Color:
{p["color"]}

Price:
${p["price"]}
"""

        )

    memory_text = (

f"""

Applied Filters

Category:
{memory["category"]}

Color:
{memory["color"]}

Brand:
{memory["brand"]}

Max Price:
{memory["max_price"]}

"""
    )
    return (memory_text + "\n" + "\n".join(result))