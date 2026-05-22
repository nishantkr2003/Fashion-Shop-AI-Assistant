memory = {}

def save_context(conversation_id,query):
    memory[conversation_id] = query


def get_context(conversation_id):
    return memory.get(conversation_id,[])