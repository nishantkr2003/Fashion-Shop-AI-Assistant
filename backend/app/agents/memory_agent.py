# def build_context(history,message):
#     if not history:
#         return message
#     recent = (history[-5:])
#     text = []
#     for m in recent:
#         text.append(f"""{m.role}:{m.content}""")

#     text.append(f"""user:{message}""")

#     return "\n".join(text)




import re


def extract_memory(history,message):
    memory = {

        "category": None,
        "color": None,
        "brand": None,
        "max_price": None

    }

    user_text = []
    for m in history:
        if m.role == "user":
            user_text.append(m.content.lower())

    user_text.append(message.lower())

    text = (" ".join(user_text))

    categories = [

        "shoes",
        "shirt",
        "watch",
        "jeans"

    ]

    colors = [

        "black",
        "white",
        "blue",
        "red"

    ]

    brands = [

        "nike",
        "adidas",
        "vans",
        "converse",
        "new balance",
        "asics"

    ]

    for c in categories:
        if c in text:
            memory["category"] = c
    for c in colors:
        if c in text:
            memory["color"] = c
    for b in brands:
        if b in text:
            memory["brand"] = b
    price = re.search(r"under\s+(\d+)",text)

    if price:
        memory["max_price"] = (float(price.group(1)))

    return memory