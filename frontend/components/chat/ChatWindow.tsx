"use client";

import { useEffect, useRef } from "react";

import { useChat } from "@/store/chatStore";

import EmptyState from "./EmptyState";

import MessageBubble from "./MessageBubble";

export default function ChatWindow() {
  const { messages } = useChat();

  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottom.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  if (messages.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="flex-1 overflow-auto p-8">
      {messages.map(
        (m,i,) => (
          <MessageBubble key={i} role={m.role} content={m.content} />),
        )}
      <div ref={bottom} />
    </div>
  );
}
