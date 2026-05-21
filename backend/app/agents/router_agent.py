def route(message: str):
    m = message.lower()

    fashion_keywords = [
        "shoe",
        "shirt",
        "pant",
        "dress",
        "product",
        "buy",
        "price",
    ]

    if any(keyword in m for keyword in fashion_keywords):
        return "sql"

    return "chat"