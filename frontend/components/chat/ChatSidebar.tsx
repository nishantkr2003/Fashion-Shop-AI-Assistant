"use client";

import { useEffect, useState } from "react";

import { getConversations, history } from "@/lib/api/chat";

import { useChat } from "@/store/chatStore";

import UserProfile from "./UserProfile";

export default function Sidebar() {
  const [items, setItems] = useState<any[]>([]);

  const { selected, setSelected, setMessages } = useChat();

  async function load() {
    const data = await getConversations();

    setItems(Array.isArray(data) ? data : []);
  }

  useEffect(() => {
    load();
  }, [selected]);

  async function open(id: number) {
    setSelected(id);

    const h = await history(id);

    setMessages(h);
  }

  return (
    <div className="w-80 border-r flex flex-col">
      <div className="p-6">
        <button className="w-full bg-black text-white rounded-xl p-3">
          + New Chat
        </button>
      </div>

      <div className="flex-1 overflow-auto">
        {items.map((i) => (
          <div
            key={i.id}
            onClick={() => open(i.id)}
            className={`p-5 cursor-pointer${selected === i.id ? "bg-gray-100" : ""}`}
          >
            {i.title}
          </div>
        ))}
      </div>

      <UserProfile />
    </div>
  );
}
