// import { create } from "zustand";

// export const useChat = create((set, get) => ({
//   selected: null,

//   messages: [],

//   setSelected: (id) =>
//     set({
//       selected: id,
//     }),

//   setMessages: (m) =>
//     set({
//       messages: typeof m === "function" ? m(get().messages) : m,
//     }),

//   add: (msg) =>
//     set((s) => ({
//       messages: [...s.messages, msg],
//     })),
// }));

import { create } from "zustand";

type Message = {
  role: string;
  content: string;
};

type ChatStore = {
  selected: number | null;

  messages: Message[];

  setSelected: (id: number | null) => void;

  setMessages: (value: Message[] | ((prev: Message[]) => Message[])) => void;

  add: (msg: Message) => void;
};

export const useChat = create<ChatStore>((set, get) => ({
  selected: null,

  messages: [],

  setSelected: (id) =>
    set({
      selected: id,
    }),

  setMessages: (value) =>
    set({
      messages: typeof value === "function" ? value(get().messages) : value,
    }),

  add: (msg) =>
    set((s) => ({
      messages: [...s.messages, msg],
    })),
}));