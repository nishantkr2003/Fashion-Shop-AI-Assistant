// const API = process.env.NEXT_PUBLIC_API_URL;

// async function parse(res: Response) {
//   if (!res.ok) {
//     throw new Error("Request failed");
//   }

//   return res.json();
// }

// export async function getConversations() {
//   try {
//     const res = await fetch(`${API}/chat/conversations`, {
//       credentials: "include",
//     });

//     return res.ok ? await parse(res) : [];
//   } catch {
//     return [];
//   }
// }

// export async function createConversation() {
//   const res = await fetch(`${API}/chat/conversation`, {
//     method: "POST",

//     credentials: "include",

//     headers: {
//       "Content-Type": "application/json",
//     },

//     body: JSON.stringify({
//       title: "New Chat",
//     }),
//   });

//   return parse(res);
// }

// export async function history(id: number) {
//   try {
//     const res = await fetch(`${API}/chat/history/${id}`, {
//       credentials: "include",
//     });

//     return res.ok ? await parse(res) : [];
//   } catch {
//     return [];
//   }
// }

// export async function streamMessage(
//   data: {
//     conversation_id: number;
//     content: string;
//   },

//   onChunk: (text: string) => void,
// ) {
//   const res = await fetch(`${API}/chat/stream`, {
//     method: "POST",

//     credentials: "include",

//     headers: {
//       "Content-Type": "application/json",
//     },

//     body: JSON.stringify(data),
//   });

//   if (!res.body) return;

//   const reader = res.body.getReader();

//   const decoder = new TextDecoder();

//   while (true) {
//     const { done, value } = await reader.read();

//     if (done) break;

//     onChunk(decoder.decode(value));
//   }
// }

const API = process.env.NEXT_PUBLIC_API_URL!;

export async function getConversations() {
  try {
    const res = await fetch(`${API}/chat/conversations`, {
      credentials: "include",
    });

    if (!res.ok) return [];

    return await res.json();
  } catch {
    return [];
  }
}



export async function createConversation() {
  const res = await fetch(`${API}/chat/conversation`, {
    method: "POST",

    credentials: "include",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      title: "New Chat",
    }),
  });

  return await res.json();
}



export async function history(id: number) {
  const res = await fetch(`${API}/chat/history/${id}`, {
    credentials: "include",
  });

  return await res.json();
}


export async function streamMessage(
  data: {
    conversation_id: number;
    content: string;
  },

  onChunk: (chunk: string) => void,
) {
  const res = await fetch(`${API}/chat/stream`, {
    method: "POST",

    credentials: "include",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(data),
  });

  if (!res.body) return;

  const reader = res.body.getReader();

  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    onChunk(decoder.decode(value,{stream:true}));
  }
}

