// "use client";

// import { useState } from "react";

// import { createConversation, streamMessage } from "@/lib/api/chat";

// import { useChat } from "@/store/chatStore";

// export default function ChatInput() {
//   const [text, setText] = useState("");

//   const [loading, setLoading] = useState(false);

//   const { selected, setSelected, add, setMessages } = useChat();

//   async function submit() {
//     if (!text.trim()) return;

//     try {
//       setLoading(true);

//       let id = selected;

//       if (!id) {
//         const c = await createConversation();

//         id = c.id;

//         setSelected(id);
//       }

//       const current = text;

//       setText("");

//       add({
//         role: "user",

//         content: current,
//       });

//       add({
//         role: "assistant",

//         content: "",
//       });

//       let streamed = "";

//       await streamMessage(
//         {
//           conversation_id: id,

//           content: current,
//         },

//         (chunk) => {
//           streamed += chunk;

//           setMessages((prev: any[]) => {
//             const copy = [...prev];

//             copy[copy.length - 1] = {
//               role: "assistant",

//               content: streamed,
//             };

//             return copy;
//           });
//         },
//       );
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="p-4 border-t flex gap-3">
//       <input
//         value={text}
//         disabled={loading}
//         placeholder="Type message..."
//         onChange={(e) => setText(e.target.value)}
//         onKeyDown={(e) => {
//           if (e.key === "Enter") submit();
//         }}
//         className="border rounded p-3 flex-1"
//       />

//       <button
//         disabled={loading}
//         onClick={submit}
//         className="border px-5 rounded"
//       >
//         {loading ? "..." : "Send"}
//       </button>
//     </div>
//   );
// }


"use client";

import { useState } from "react";

import { createConversation, streamMessage } from "@/lib/api/chat";

import { useChat } from "@/store/chatStore";

export default function ChatInput() {
  const [text, setText] = useState("");

  const [loading, setLoading] = useState(false);

  const { selected, setSelected, add, setMessages } = useChat();

  async function submit() {
    if (!text) return;

    setLoading(true);

    try {
      let id = selected;

      if (!id) {
        const c = await createConversation();

        id = c.id;

        setSelected(id);
      }

      const current = text;

      setText("");

      add({
        role: "user",

        content: current,
      });

      add({
        role: "assistant",

        content: "",
      });

      let stream = "";

      await streamMessage(
        {
          conversation_id: id,

          content: current,
        },

        (chunk) => {
          stream += chunk;

          setMessages((prev) => {
            const copy = [...prev];

            copy[copy.length - 1] = {
              role: "assistant",

              content: stream + "▋",
            };

            return copy;
          });
        },
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border-t p-5">
      <div className="flex gap-3">
        <input
          value={text}
          disabled={loading}
          placeholder="Ask anything…"
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              submit();
            }
          }}
          className="flex-1 rounded-2xl border p-4"/>

        <button
          onClick={submit}
          disabled={loading}
          className="px-6 rounded-2xl g-black text-white">
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}