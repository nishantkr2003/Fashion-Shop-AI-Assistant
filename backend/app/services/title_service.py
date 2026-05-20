async def generate_title(text:str):
    words = (text.split())
    title = (" ".join(words[:4]))
    return (title or "New Chat")